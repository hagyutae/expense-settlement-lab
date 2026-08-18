from core.domain.rules.r010_receipt_no_duplicated import R010


def test_r010(settle):
    result = settle([R010()], "r010.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R010"], ["R010"], [], []]
