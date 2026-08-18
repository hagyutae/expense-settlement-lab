from core.domain.rules.r005_receipt_no_missing import R005


def test_r005(settle):
    result = settle([R005()], "r005.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R005"], ["R005"], [], []]
