<div align="center">

# VulnSight 🔭

**AI-powered vulnerability report analyzer**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version](https://img.shields.io/github/v/release/xiabai2004/VulnSight?include_prereleases&logo=github)](https://github.com/xiabai2004/VulnSight/releases)
[![CI](https://github.com/xiabai2004/VulnSight/actions/workflows/ci.yml/badge.svg)](https://github.com/xiabai2004/VulnSight/actions)
[![GitHub stars](https://img.shields.io/github/stars/xiabai2004/VulnSight?style=social)](https://github.com/xiabai2004/VulnSight/stargazers)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Turn RayScan scanner output into beautiful, human-readable fix reports with AI-powered analysis.**

English · [中文](README.zh.md)

</div>

---

## Overview

VulnSight bridges the gap between security scanners and developers. It reads RayScan's JSON report and generates structured fix reports with explanations, impact assessments, and code examples — making it easy for developers to understand and remediate vulnerabilities.

```
RayScan scans → JSON results → VulnSight analyzes → 📄 Beautiful report (HTML / Markdown)
                                                          ↓
                                               Developers fix by the guide
```

## Features

- ✅ **Parses RayScan reports** — Supports SQLi, XSS, LFI, SSRF, CMDi, XXE, RCE, and more
- 🤖 **AI-powered analysis** — Uses LLM (DeepSeek / OpenAI) to generate in-depth fix suggestions
- 📦 **Built-in fix templates** — Does NOT require an API key; falls back to expert-written guides
- 🎨 **Beautiful HTML reports** — Collapsible cards, severity badges, code samples
- 📝 **Markdown reports** — Great for wikis, pull requests, and blog posts
- 📂 **Batch processing** — Analyze entire directories of scan reports in one command

## Quick Start

```bash
# Install
pip install git+https://github.com/xiabai2004/VulnSight.git

# Or local development
git clone https://github.com/xiabai2004/VulnSight.git
cd VulnSight
pip install -e .
```

### Basic Usage

```bash
# Analyze a report with built-in templates (no API key needed)
vulnsight scan_reports/report.json -o report.html

# Quick overview of a directory
vulnsight scan_reports/ --summary

# AI-powered analysis
export VULSENSE_API_KEY=sk-your-key
vulnsight report.json --ai -o report.html

# Markdown output
vulnsight report.json -o report.md --format md
```

## Report Preview

Generated HTML reports include:

- 📊 **Statistics cards** — High / Medium / Low / Info counts at a glance
- 🏷️ **Vulnerability type grid** — See which bugs are most common
- 🔍 **Expandable analysis cards** — One per vulnerability
- 💥 **Impact assessment** — What could go wrong if left unfixed?
- 🔧 **Fix suggestions** — Wrong vs. correct code side-by-side

## Requirements

| Dependency | Minimum Version |
|------------|-----------------|
| Python     | 3.9+            |
| requests   | 2.28+           |
| rich       | 13.0+           |
| Jinja2     | 3.1+            |
| markdown   | 3.4+            |

An LLM API key (DeepSeek / OpenAI) is optional — enables AI-powered analysis.

## Architecture

```
vulnsight/
├── parser.py      # RayScan JSON report parser
├── analyzer.py    # AI analysis engine + fallback fix templates
├── reporter.py    # HTML / Markdown report generator
├── cli.py         # Command-line interface
└── config.py      # Configuration
```

## Roadmap

- [x] HTML report with interactive collapse cards
- [ ] Support for Burp Suite and Nuclei scanner formats
- [ ] PDF export
- [ ] CI/CD integration (GitHub Action)
- [ ] VSCode extension for inline vulnerability hints

## Related Projects

- [RayScan](https://github.com/xiabai2004/RayScan) — Web vulnerability scanner (feeds VulnSight)
- [SecuBot](https://github.com/xiabai2004/SecuBot) — AI security ops agent (orchestrates RayScan + VulnSight)

## License

MIT — see [LICENSE](LICENSE) for details.
