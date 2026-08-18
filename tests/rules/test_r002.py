from core.domain.rules.r002_amount_valid import R002


def test_r002(settle):
    result = settle([R002()], "r002.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R002"], ["R002"], [], []]
