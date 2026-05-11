# VulnSight 🔭

**AI-powered vulnerability report analyzer** — Turn RayScan scan results into human-readable fix reports with code examples.

```
RayScan scans → JSON report → VulnSight analyzes → 📄 Beautiful HTML/MD report
                                                                ↓
                                                     Developers fix by the guide
```

## Features

- **Parses RayScan JSON reports** — SQLi, XSS, LFI, SSRF, CMDi, XXE, RCE, and more
- **AI-powered analysis** — Uses LLM (DeepSeek/OpenAI) to analyze each vulnerability
- **Built-in fix templates** — Falls back to expert-written fix guides when no API key
- **Beautiful HTML reports** — Collapsible cards, severity badges, code examples
- **Markdown reports** — Great for embedding in wikis or blog posts
- **Batch processing** — Analyze entire directories of scan reports

## Quick Start

```bash
# Install
pip install -e .

# Analysis with built-in templates (no API key needed)
vulnsight scan_reports/report.json -o report.html

# Quick overview of all reports
vulnsight scan_reports/ --summary

# AI-powered analysis
export VULSENSE_API_KEY=sk-your-key
vulnsight report.json --ai -o report.html

# Markdown output
vulnsight report.json -o report.md --format md
```

## Sample Report

Generated reports include:
- 📊 **Vulnerability stats** — High/Medium/Low/Info counts
- 🏷️ **Type distribution** — See which vulns are most common
- 🔍 **Detailed analysis** — Collapsible cards per vulnerability
- 💥 **Impact assessment** — What could go wrong?
- 🔧 **Fix suggestions** — Wrong vs correct code examples

## Architecture

```
vulnsight/
├── parser.py      # RayScan JSON report parser
├── analyzer.py    # AI analysis engine + fallback templates
├── reporter.py    # HTML/Markdown report generator
├── cli.py         # Command-line interface
└── config.py      # Configuration
```

## Requirements

- Python 3.9+
- Optional: LLM API key (DeepSeek / OpenAI)

## Roadmap

- [ ] Support for other scanner formats (Burp Suite, Nuclei)
- [x] HTML report with interactive cards
- [ ] PDF export
- [ ] CI/CD integration (GitHub Action)

## License

MIT

---

*Part of the RayScan ecosystem. Scan with RayScan, analyze with VulnSight.*
