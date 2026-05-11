"""RayScan JSON 报告解析器"""

import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Vulnerability:
    type: str
    url: str
    parameter: Optional[str]
    module: str
    severity: str
    evidence: str
    payload: str

    @property
    def severity_level(self) -> int:
        return {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}.get(self.severity, 0)

    @property
    def type_cn(self) -> str:
        type_map = {
            "sql_injection": "SQL 注入",
            "cross_site_scripting": "跨站脚本 (XSS)",
            "local_file_inclusion": "本地文件包含 (LFI)",
            "remote_file_inclusion": "远程文件包含 (RFI)",
            "command_injection": "命令注入 (CMDi)",
            "server_side_request_forgery": "服务端请求伪造 (SSRF)",
            "xee": "XML 外部实体注入 (XXE)",
            "rce": "远程代码执行 (RCE)",
            "information_disclosure": "信息泄露",
            "insecure_configuration": "不安全配置",
            "sensitive_data_exposure": "敏感数据暴露",
            "open_redirect": "开放重定向",
            "csrf": "跨站请求伪造 (CSRF)",
            "path_traversal": "路径遍历",
        }
        return type_map.get(self.type, self.type)


@dataclass
class ScanReport:
    tool: str
    target: str
    scan_time: str
    duration_seconds: float
    total_vulnerabilities: int
    vulnerabilities_by_type: dict
    vulnerabilities: list[Vulnerability] = field(default_factory=list)

    @property
    def duration_str(self) -> str:
        m, s = divmod(int(self.duration_seconds), 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h}h{m}m{s}s"
        elif m:
            return f"{m}m{s}s"
        return f"{s}s"

    @property
    def severity_summary(self) -> dict:
        summary = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for v in self.vulnerabilities:
            if v.severity in summary:
                summary[v.severity] += 1
        return summary


def parse_file(path: str | Path) -> ScanReport:
    """解析单个 RayScan JSON 报告文件"""
    path = Path(path)
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)

    vulns = []
    for v in data.get("vulnerabilities", []):
        try:
            vulns.append(Vulnerability(**v))
        except TypeError:
            # 某些报告缺少字段时自动补全
            vulns.append(Vulnerability(
                type=v.get("type", "unknown"),
                url=v.get("url", ""),
                parameter=v.get("parameter"),
                module=v.get("module", ""),
                severity=v.get("severity", "info"),
                evidence=v.get("evidence", ""),
                payload=v.get("payload", ""),
            ))

    return ScanReport(
        tool=data.get("tool", "RayScan"),
        target=data.get("target", ""),
        scan_time=data.get("scan_time", ""),
        duration_seconds=data.get("duration_seconds", 0),
        total_vulnerabilities=data.get("total_vulnerabilities", len(vulns)),
        vulnerabilities_by_type=data.get("vulnerabilities_by_type", {}),
        vulnerabilities=vulns,
    )


def parse_directory(dir_path: str | Path) -> list[ScanReport]:
    """解析目录下所有 RayScan JSON 报告"""
    dir_path = Path(dir_path)
    reports = []
    for f in sorted(dir_path.glob("*.json")):
        try:
            reports.append(parse_file(f))
        except Exception as e:
            print(f"  ⚠️  跳过 {f.name}: {e}")
    return reports
