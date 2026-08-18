from core.domain.rules.r013_weekend_preapproval import R013


def test_r013(settle):
    result = settle([R013()], "r013.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R013"], ["R013"], [], []]
