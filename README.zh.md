<div align="center">

# VulnSight 🔭

**AI 驱动的漏洞报告分析器**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version](https://img.shields.io/github/v/release/xiabai2004/VulnSight?include_prereleases&logo=github)](https://github.com/xiabai2004/VulnSight/releases)
[![CI](https://github.com/xiabai2004/VulnSight/actions/workflows/ci.yml/badge.svg)](https://github.com/xiabai2004/VulnSight/actions)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**把 RayScan 扫描结果变成漂亮、可读的修复报告，支持 AI 分析。**

[English](README.md) · 中文

</div>

---

## 概述

VulnSight 填补了安全扫描器和开发者之间的鸿沟。它读取 RayScan 的 JSON 报告，生成结构化的修复报告，包含漏洞说明、影响评估和代码示例——让开发者轻松理解并修复安全漏洞。

```
RayScan 扫描 → JSON 结果 → VulnSight 分析 → 📄 精美报告 (HTML / Markdown)
                                                     ↓
                                         开发者照着修复指南改
```

## 功能特性

- ✅ **解析 RayScan 报告** — 支持 SQL注入、XSS、LFI、SSRF、命令注入、XXE、RCE 等
- 🤖 **AI 分析** — 调用 DeepSeek / OpenAI LLM 生成深度修复建议
- 📦 **内置修复模板** — 不需要 API Key，自带专家编写的修复指南
- 🎨 **精美 HTML 报告** — 可折叠卡片、严重程度徽标、代码示例
- 📝 **Markdown 报告** — 适合嵌入 Wiki、PR 和博客文章
- 📂 **批量处理** — 一键分析整个目录的扫描报告

## 快速开始

```bash
# 安装
pip install git+https://github.com/xiabai2004/VulnSight.git

# 本地开发
git clone https://github.com/xiabai2004/VulnSight.git
cd VulnSight
pip install -e .
```

### 基本用法

```bash
# 用内置模板分析（无需 API Key）
vulnsight scan_reports/report.json -o report.html

# 目录快速概览
vulnsight scan_reports/ --summary

# AI 分析
export VULSENSE_API_KEY=sk-your-key
vulnsight report.json --ai -o report.html

# Markdown 输出
vulnsight report.json -o report.md --format md
```

## 报告预览

生成的 HTML 报告包含：

- 📊 **统计卡片** — 高危 / 中危 / 低危 / 信息 一览无余
- 🏷️ **漏洞类型网格** — 直观看到哪个漏洞最多
- 🔍 **可展开分析卡片** — 每个漏洞一个
- 💥 **影响评估** — 不修的话会怎样？
- 🔧 **修复方案** — 错误写法 vs 正确写法对比

## 系统要求

| 依赖 | 最低版本 |
|------|---------|
| Python | 3.9+ |
| requests | 2.28+ |
| rich | 13.0+ |
| Jinja2 | 3.1+ |
| markdown | 3.4+ |

LLM API Key（DeepSeek / OpenAI）可选——启用后可使用 AI 分析。

## 技术架构

```
vulnsight/
├── parser.py      # RayScan JSON 报告解析器
├── analyzer.py    # AI 分析引擎 + 保底修复模板
├── reporter.py    # HTML / Markdown 报告生成器
├── cli.py         # 命令行入口
└── config.py      # 配置管理
```

## 开发路线

- [x] 可折叠交互卡片的 HTML 报告
- [ ] 支持 Burp Suite 和 Nuclei 扫描格式
- [ ] PDF 导出
- [ ] CI/CD 集成（GitHub Action）
- [ ] VSCode 扩展（行内漏洞提示）

## 相关项目

- [RayScan](https://github.com/xiabai2004/RayScan) — Web 漏洞扫描器（VulnSight 的数据源）
- [SecuBot](https://github.com/xiabai2004/SecuBot) — AI 安全运营 Agent（编排 RayScan + VulnSight）

## 许可

MIT — 详见 [LICENSE](LICENSE)
