"""VulnSight CLI -- command-line interface"""

import argparse
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from . import __version__  # noqa: E402
from .parser import parse_file, parse_directory  # noqa: E402
from .analyzer import Analyzer  # noqa: E402
from .reporter import generate_html, generate_markdown, save_report  # noqa: E402


EPILOG = """
Examples:
  # Analyze a single report
  vulnsight scan_reports/report.json

  # Analyze an entire directory
  vulnsight scan_reports/

  # Output HTML report
  vulnsight report.json -o report.html

  # AI-powered analysis (set VULSENSE_API_KEY env var)
  export VULSENSE_API_KEY=sk-your-key
  vulnsight report.json --ai

  # Markdown output
  vulnsight report.json -o report.md --format md

  # Just show summary
  vulnsight report.json --summary
"""


def main():
    parser = argparse.ArgumentParser(
        prog="vulnsight",
        description="VulnSight -- AI-powered vulnerability report analyzer",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("input", help="RayScan JSON report file or directory")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument(
        "--format", choices=["html", "md", "markdown"],
        default="html", help="Output format (default: html)"
    )
    parser.add_argument(
        "--ai", action="store_true",
        help="Enable AI analysis (requires VULSENSE_API_KEY env var)"
    )
    parser.add_argument("--summary", action="store_true", help="Show summary only")
    parser.add_argument("--model", default="deepseek-chat", help="LLM model name")
    parser.add_argument("-V", "--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        print(f"VulnSight v{__version__}")
        return

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: path not found: {input_path}")
        sys.exit(1)

    print(f"Parsing: {input_path.name if input_path.is_file() else str(input_path)}")
    if input_path.is_file():
        reports = [parse_file(input_path)]
    else:
        reports = parse_directory(input_path)

    if not reports:
        print("Error: no valid reports found")
        sys.exit(1)

    total_vulns = sum(r.total_vulnerabilities for r in reports)
    print(f"Found {len(reports)} report(s), {total_vulns} vulnerabilities\n")

    for r in reports:
        sev = r.severity_summary
        high = sev.get("critical", 0) + sev.get("high", 0)
        print(f"  Target: {r.target}")
        print(f"  Time: {r.scan_time} | Duration: {r.duration_str}")
        print(f"  Total: {r.total_vulnerabilities} (High: {high}, "
              f"Med: {sev.get('medium', 0)}, Low: {sev.get('low', 0)}, Info: {sev.get('info', 0)})")
        print()

    if args.summary:
        return

    print("Analyzing vulnerabilities...")
    analyzer = Analyzer(api_key=None if not args.ai else None)

    for report in reports:
        result = analyzer.analyze_report(report)

        fmt = args.format
        if args.output:
            out_path = Path(args.output)
            if out_path.suffix == ".md":
                fmt = "md"
            elif out_path.suffix == ".html":
                fmt = "html"
        else:
            stem = Path(input_path).stem
            out_path = f"{stem}_vulnsight.html"
            if fmt in ("md", "markdown"):
                out_path = f"{stem}_vulnsight.md"

        output = generate_markdown(result) if fmt in ("md", "markdown") else generate_html(result, __version__)
        saved = save_report(output, out_path)
        print(f"Report saved: {saved}")

    print(f"\nDone! {total_vulns} vulnerabilities analyzed.")


if __name__ == "__main__":
    main()
