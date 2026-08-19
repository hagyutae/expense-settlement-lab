"""집계 연산.

구현체가 조합해 쓰는 필터와 계산입니다. **반올림은 여기서 한 번만 합니다.**
표현 계층이 다시 나누면 터미널과 웹에서 숫자가 갈립니다.
"""


def select(judgements, department=None, expense_type=None, passed=None, month=None):
    """조건에 맞는 판정만 거릅니다. 주지 않은 조건은 보지 않습니다."""
    picked = list(judgements)
    if department is not None:
        picked = [j for j in picked if j.expense.department == department]
    if expense_type is not None:
        picked = [j for j in picked if j.expense.expense_type == expense_type]
    if passed is not None:
        picked = [j for j in picked if j.is_passed == passed]
    if month is not None:
        picked = [
            j for j in picked
            if j.expense.used_date is not None
            and j.expense.used_date.strftime("%Y-%m") == month
        ]
    return picked


def count(judgements):
    return len(list(judgements))


def total_amount(judgements):
    """금액 합계. `amount` 가 비었으면 0으로 봅니다."""
    return sum(j.expense.amount or 0 for j in judgements)


def ratio(part, whole):
    """백분율. 소수점 첫째 자리에서 반올림하고, 분모가 0이면 `0.0` 입니다."""
    if not whole:
        return 0.0
    return round(part / whole * 100, 1)
