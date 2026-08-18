from core.domain.rules.r018_cash_limit import R018


def test_r018(settle):
    result = settle([R018()], "r018.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R018"], ["R018"], [], []]
