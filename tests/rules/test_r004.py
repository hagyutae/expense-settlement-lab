from core.domain.rules.r004_claim_deadline import R004


def test_r004(settle):
    result = settle([R004()], "r004.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R004"], ["R004"], [], []]
