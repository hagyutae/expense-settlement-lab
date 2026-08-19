"""CLI 진입점.

    uv run settle samples\\영업1팀.csv
    uv run settle samples\\영업1팀.csv --in csv --out console

`main` 이름은 바꾸지 마세요. pyproject.toml 의 `settle` 명령이 이 함수를 가리킵니다.
"""

import argparse
import sys
from pathlib import Path

from application.container import build_loader, build_reporter, build_service


def main():
    parser = argparse.ArgumentParser(prog="settle", description="경비 청구 파일을 검증합니다.")
    parser.add_argument("path", help="경비 청구 파일 경로")
    parser.add_argument("--in", dest="fmt_in", default=None, help="입력 형식. 생략하면 확장자로 판단")
    parser.add_argument("--out", dest="fmt_out", default="console", help="출력 형식")
    parser.add_argument("--save", dest="save", default=None, help="결과를 저장할 파일 경로")
    args = parser.parse_args()

    # 확장자로 형식을 정하는 일은 진입점의 몫이다. 조립은 형식 이름만 받는다.
    fmt_in = args.fmt_in or Path(args.path).suffix.lstrip(".").lower()

    try:
        loader = build_loader(fmt_in)
        reporter = build_reporter(args.fmt_out)
        expenses = loader.load(args.path)
    except (OSError, ValueError) as e:
        print(e, file=sys.stderr)
        return 1

    text = reporter.format(build_service().settle(expenses))

    # 리포터는 문자열만 돌려준다. 파일로 남기는 일은 진입점이 맡는다.
    if args.save:
        target = Path(args.save)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        print(f"저장했습니다: {args.save}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
