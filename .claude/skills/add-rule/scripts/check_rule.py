#!/usr/bin/env python3
"""규칙 하나가 연동 지점 네 곳에 모두 반영됐는지 확인합니다.

규칙 코드를 하나 받아 아래 네 곳을 훑고, 빠진 곳이 있으면 알립니다.

1. 규칙 구현   src/core/domain/rules/rXXX_*.py
2. 테스트      tests/rules/test_rXXX.py
3. 픽스처      tests/rules/fixtures/rXXX.csv
4. 레지스트리  @rule 데코레이터. 조립은 load_rules() 가 맡습니다

사용: uv run python check_rule.py R011
빠진 곳이 하나라도 있으면 종료 코드 1 로 끝냅니다.
"""

import re
import sys
from pathlib import Path


def find_root(start):
    """src/core/domain/rules 를 품은 상위 폴더를 저장소 루트로 봅니다."""
    for base in (start, *start.parents):
        if (base / "src" / "core" / "domain" / "rules").is_dir():
            return base
    return start


def normalize(arg):
    """r11, R011, 011 같은 입력을 파일용 rXXX 와 클래스용 RXXX 로 맞춥니다."""
    digits = re.sub(r"\D", "", arg)
    if not digits:
        raise ValueError(f"규칙 코드에서 숫자를 찾지 못했습니다: {arg}")
    num = f"{int(digits):03d}"
    return f"r{num}", f"R{num}"


def registered_in(path, cls):
    """`@rule` 이 클래스 바로 위에 붙어 있으면 등록된 것으로 봅니다."""
    if not path.is_file():
        return False, f"{path} 파일이 없습니다"
    text = path.read_text(encoding="utf-8")
    if re.search(rf"@rule\s*\nclass\s+{cls}\b", text) is None:
        return False, "@rule 데코레이터 없음"
    if re.search(r"from core\.domain\.rules\.registry import rule", text) is None:
        return False, "registry import 없음"
    return True, "@rule 확인"


def check(root, low, cls):
    """네 곳을 (이름, 통과 여부, 설명) 목록으로 돌려줍니다."""
    results = []

    matches = sorted((root / "src/core/domain/rules").glob(f"{low}_*.py"))
    if matches:
        results.append(("규칙 구현", True, matches[0].name))
    else:
        results.append(("규칙 구현", False, f"{low}_*.py 파일이 없습니다"))

    test = root / "tests/rules" / f"test_{low}.py"
    results.append(("테스트", test.is_file(),
                    test.name if test.is_file() else f"test_{low}.py 파일이 없습니다"))

    fixture = root / "tests/rules/fixtures" / f"{low}.csv"
    results.append(("픽스처", fixture.is_file(),
                    fixture.name if fixture.is_file() else f"{low}.csv 파일이 없습니다"))

    source = matches[0] if matches else root / "src/core/domain/rules" / f"{low}_.py"
    results.append(("레지스트리", *registered_in(source, cls)))

    return results


def main(argv):
    if len(argv) != 2:
        print("사용: uv run python check_rule.py <규칙 코드>", file=sys.stderr)
        return 2
    try:
        low, cls = normalize(argv[1])
    except ValueError as err:
        print(err, file=sys.stderr)
        return 2

    root = find_root(Path.cwd())
    results = check(root, low, cls)

    print(f"{cls} 연동 지점 점검")
    for name, ok, detail in results:
        mark = "OK  " if ok else "빠짐"
        print(f"  [{mark}] {name}: {detail}")

    missing = [name for name, ok, _ in results if not ok]
    if missing:
        print(f"\n빠진 곳 {len(missing)}: {', '.join(missing)}")
        return 1
    print("\n네 곳 모두 반영됐습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
