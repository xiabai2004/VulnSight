"""AI 漏洞分析引擎 — 调用 LLM 分析漏洞并生成修复建议"""

import json
import os
import requests
from typing import Optional
from .parser import Vulnerability, ScanReport


# 漏洞修复知识库 — LLM 不可用时的保底方案
FIX_TEMPLATES = {
    "sql_injection": {
        "title": "SQL 注入修复指南",
        "fix": "使用参数化查询 / prepared statement，禁止拼接 SQL",
        "code": (
            "# ❌ 错误：字符串拼接\n"
            "cursor.execute(f\"SELECT * FROM users WHERE id = {user_input}\")\n\n"
            "# ✅ 正确：参数化查询\n"
            "cursor.execute(\"SELECT * FROM users WHERE id = ?\", (user_input,))"
        ),
        "references": ["OWASP SQL Injection Prevention Cheat Sheet"],
    },
    "cross_site_scripting": {
        "title": "XSS 修复指南",
        "fix": "对用户输入进行 HTML 实体编码 + Content-Security-Policy 头",
        "code": (
            "# ❌ 错误：直接输出用户输入\n"
            "return f\"<div>{user_input}</div>\"\n\n"
            "# ✅ 正确：HTML 实体编码\n"
            "import html\n"
            "return f\"<div>{html.escape(user_input)}</div>\""
        ),
        "references": ["OWASP XSS Prevention Cheat Sheet"],
    },
    "local_file_inclusion": {
        "title": "本地文件包含修复指南",
        "fix": "白名单校验文件路径，禁止用户控制文件路径参数",
        "code": (
            "# ❌ 错误：直接拼接用户输入\n"
            "include($_GET['page']);\n\n"
            "# ✅ 正确：白名单校验\n"
            "$allowed = ['home', 'about', 'contact'];\n"
            "$page = in_array($_GET['page'], $allowed) ? $_GET['page'] : 'home';\n"
            "include(\"pages/{$page}.php\");"
        ),
        "references": ["OWASP File Inclusion Prevention"],
    },
    "server_side_request_forgery": {
        "title": "SSRF 修复指南",
        "fix": "白名单限制请求目标，禁止访问内网地址段",
        "code": (
            "# ❌ 错误：允许用户指定任意 URL\n"
            "response = requests.get(user_url)\n\n"
            "# ✅ 正确：白名单 + IP 校验\n"
            "from urllib.parse import urlparse\n"
            "ALLOWED_HOSTS = ['api.example.com']\n"
            "parsed = urlparse(user_url)\n"
            "if parsed.hostname not in ALLOWED_HOSTS:\n"
            "    raise ValueError('Invalid target')"
        ),
        "references": ["OWASP SSRF Prevention"],
    },
    "command_injection": {
        "title": "命令注入修复指南",
        "fix": "使用安全的 API 替代系统命令执行，严格校验输入",
        "code": (
            "# ❌ 错误：直接拼接系统命令\n"
            "os.system(f\"ping {user_input}\")\n\n"
            "# ✅ 正确：使用安全库代替\n"
            "import subprocess\n"
            "subprocess.run(['ping', '-c', '4', user_input], check=True)"
        ),
        "references": ["OWASP Command Injection Prevention"],
    },
    "information_disclosure": {
        "title": "信息泄露修复指南",
        "fix": "移除响应中的版本信息、错误堆栈、内部路径等敏感数据",
        "code": (
            "# 生产环境关闭调试模式\n"
            "# Django: DEBUG = False\n"
            "# Flask: app.config['DEBUG'] = False\n"
            "# Nginx: server_tokens off;\n\n"
            "# 移除响应头中的版本信息\n"
            "# Apache: ServerSignature Off\n"
            "# Nginx: server_tokens off;"
        ),
        "references": ["OWASP Information Disclosure"],
    },
    "insecure_configuration": {
        "title": "不安全配置修复指南",
        "fix": "移除默认凭据、禁用不必要的服务、启用安全配置",
        "code": (
            "# 修改默认凭据\n"
            "# 禁用目录列表\n"
            "# Apache: Options -Indexes\n"
            "# Nginx: autoindex off;\n\n"
            "# 移除不必要的信息泄露端点\n"
            "# 如 /info.php, /phpinfo.php, /server-status"
        ),
        "references": ["OWASP Security Configuration"],
    },
}


def _get_vuln_fix(vuln_type: str) -> dict:
    """获取漏洞类型对应的修复模板"""
    base_type = vuln_type.replace(" ", "_").lower()
    if base_type in FIX_TEMPLATES:
        return FIX_TEMPLATES[base_type]
    return {
        "title": f"{vuln_type} 修复建议",
        "fix": "对相关输入进行严格校验和清理",
        "code": "# 严格校验输入\nvalidate_input(user_input)\nsanitize_output(output)",
        "references": ["OWASP Cheat Sheet Series"],
    }


class Analyzer:
    """漏洞分析引擎"""

    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-chat"):
        self.api_key = api_key or os.getenv("VULSENSE_API_KEY")
        self.model = model
        self.use_llm = bool(self.api_key)
        if not self.api_key:
            print("  ⚠️  未设置 VULSENSE_API_KEY，将使用内置模板分析")

    def analyze_vulnerability(self, vuln: Vulnerability) -> dict:
        """分析单个漏洞，返回分析结果"""
        if self.use_llm:
            return self._analyze_with_llm(vuln)
        return self._analyze_with_template(vuln)

    def _analyze_with_template(self, vuln: Vulnerability) -> dict:
        """使用内置模板分析"""
        fix = _get_vuln_fix(vuln.type)
        return {
            "type": vuln.type,
            "severity": vuln.severity,
            "description": f"发现 {vuln.type_cn} 漏洞",
            "impact": self._get_impact(vuln),
            "fix_title": fix["title"],
            "fix_summary": fix["fix"],
            "code_example": fix["code"],
            "references": fix["references"],
            "source": "template",
        }

    def _get_impact(self, vuln: Vulnerability) -> str:
        impacts = {
            "critical": "可导致服务器完全被控制，数据全部泄露",
            "high": "可导致敏感数据被获取或服务被篡改",
            "medium": "可导致部分信息泄露或功能被绕过",
            "low": "影响有限，但仍建议修复",
            "info": "仅为信息提示，无直接安全风险",
        }
        return impacts.get(vuln.severity, "存在安全风险")

    def _analyze_with_llm(self, vuln: Vulnerability) -> dict:
        """调用 LLM 分析漏洞"""
        prompt = f"""你是一个专业的安全工程师。分析以下漏洞并提供详细的修复建议。

漏洞信息：
- 类型：{vuln.type_cn} ({vuln.type})
- 严重程度：{vuln.severity}
- 目标 URL：{vuln.url}
- 参数：{vuln.parameter or 'N/A'}
- 检测模块：{vuln.module}
- 证据：{vuln.evidence[:200] if vuln.evidence else 'N/A'}
- Payload：{vuln.payload[:200] if vuln.payload else 'N/A'}

请返回 JSON 格式：
{{
  "description": "漏洞描述（中文，通俗易懂）",
  "impact": "漏洞可能导致的后果",
  "fix_summary": "修复方案概述",
  "code_example": "修复代码示例（含错误写法对比）",
  "references": ["参考链接"]
}}"""

        try:
            resp = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 1000,
                },
                timeout=30,
            )
            resp.raise_for_status()
            result = resp.json()
            content = result["choices"][0]["message"]["content"]

            # Extract JSON from response
            content = content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1]
                content = content.rsplit("```", 1)[0]
            analysis = json.loads(content)

            analysis.update({
                "type": vuln.type,
                "severity": vuln.severity,
                "fix_title": f"{vuln.type_cn} 修复方案",
                "source": "llm",
            })
            return analysis

        except Exception as e:
            print(f"  ⚠️  LLM 分析失败 ({e})，降级到模板分析")
            return self._analyze_with_template(vuln)

    def analyze_report(self, report: ScanReport) -> dict:
        """分析完整扫描报告"""
        results = []
        for vuln in report.vulnerabilities:
            results.append(self.analyze_vulnerability(vuln))

        return {
            "report_summary": {
                "target": report.target,
                "scan_time": report.scan_time,
                "duration": report.duration_str,
                "total": report.total_vulnerabilities,
                "by_type": report.vulnerabilities_by_type,
                "by_severity": report.severity_summary,
            },
            "analyses": results,
        }
