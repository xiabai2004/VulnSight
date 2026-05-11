"""VulnSight CLI 鈥?鍛戒护琛屽叆鍙?""

import argparse
import sys
import io
from pathlib import Path

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from . import __version__
from .parser import parse_file, parse_directory
from .analyzer import Analyzer
from .reporter import generate_html, generate_markdown, save_report


EPILOG = """
绀轰緥:
  # 鍒嗘瀽鍗曚釜鎶ュ憡
  vulnsight scan_reports/report.json

  # 鍒嗘瀽鏁翠釜鐩綍
  vulnsight scan_reports/

  # 杈撳嚭 HTML 鎶ュ憡
  vulnsight report.json -o report.html

  # 璁剧疆 API Key 鍚敤 AI 鍒嗘瀽
  export VULSENSE_API_KEY=your-api-key
  vulnsight report.json --ai

  # 杈撳嚭 Markdown
  vulnsight report.json -o report.md --format md

  # 鏌ョ湅鎶ュ憡姒傝
  vulnsight report.json --summary
"""


def main():
    parser = argparse.ArgumentParser(
        prog="vulnsight",
        description="VulnSight 鈥?AI-powered vulnerability report analyzer 馃洝锔?,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "input",
        help="RayScan JSON 鎶ュ憡鏂囦欢鎴栫洰褰?,
    )
    parser.add_argument(
        "-o", "--output",
        help="杈撳嚭鏂囦欢璺緞锛堣嚜鍔ㄦ牴鎹悗缂€鍐冲畾鏍煎紡锛?,
    )
    parser.add_argument(
        "--format", choices=["html", "md", "markdown"],
        default="html",
        help="杈撳嚭鏍煎紡锛堥粯璁?html锛?,
    )
    parser.add_argument(
        "--ai", action="store_true",
        help="鍚敤 AI 鍒嗘瀽锛堥渶璁剧疆 VULSENSE_API_KEY 鐜鍙橀噺锛?,
    )
    parser.add_argument(
        "--summary", action="store_true",
        help="浠呮樉绀烘瑙堟憳瑕?,
    )
    parser.add_argument(
        "--model", default="deepseek-chat",
        help="LLM 妯″瀷鍚嶇О锛堥粯璁?deepseek-chat锛?,
    )
    parser.add_argument(
        "-V", "--version", action="store_true",
        help="鏄剧ず鐗堟湰淇℃伅",
    )

    args = parser.parse_args()

    if args.version:
        print(f"VulnSight v{__version__}")
        return

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"鉂?杈撳叆璺緞涓嶅瓨鍦? {input_path}")
        sys.exit(1)

    # 瑙ｆ瀽鎶ュ憡
    print(f"馃搨 姝ｅ湪瑙ｆ瀽: {input_path.name if input_path.is_file() else str(input_path)}")
    if input_path.is_file():
        reports = [parse_file(input_path)]
    else:
        reports = parse_directory(input_path)

    if not reports:
        print("鉂?鏈壘鍒版湁鏁堟姤鍛?)
        sys.exit(1)

    # 鏄剧ず姒傝
    print(f"馃搳 鍏?{len(reports)} 涓姤鍛婏紝{sum(r.total_vulnerabilities for r in reports)} 涓紡娲瀄n")

    for r in reports:
        sev = r.severity_summary
        high = sev.get("critical", 0) + sev.get("high", 0)
        print(f"  馃搫 {r.target}")
        print(f"     鈴?{r.scan_time} | 鑰楁椂 {r.duration_str}")
        print(f"     馃悰 鍏?{r.total_vulnerabilities} 涓紡娲?)
        print(f"        楂樺嵄 {high} | 涓嵄 {sev.get('medium',0)} | 浣庡嵄 {sev.get('low',0)} | 淇℃伅 {sev.get('info',0)}")
        print()

    if args.summary:
        return

    # 鍒嗘瀽
    print("馃敩 姝ｅ湪鍒嗘瀽婕忔礊...")
    analyzer = Analyzer(api_key=None if not args.ai else None)

    for report in reports:
        result = analyzer.analyze_report(report)

        # 鐢熸垚鎶ュ憡
        format = args.format
        if args.output:
            out_path = Path(args.output)
            if out_path.suffix == ".md":
                format = "md"
            elif out_path.suffix == ".html":
                format = "html"
        else:
            out_path = input_path.stem + "_vulnsight.html"
            if format in ("md", "markdown"):
                out_path = input_path.stem + "_vulnsight.md"

        if format in ("md", "markdown"):
            output = generate_markdown(result)
        else:
            output = generate_html(result, __version__)

        saved = save_report(output, out_path)
        print(f"鉁?鎶ュ憡宸茬敓鎴? {saved}")

    print(f"\n鉁?鍒嗘瀽瀹屾垚锛佸叡 {sum(r.total_vulnerabilities for r in reports)} 涓紡娲炲垎鏋愬畬姣?)


if __name__ == "__main__":
    main()
