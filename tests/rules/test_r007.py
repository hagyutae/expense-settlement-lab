from core.domain.rules.r007_lodging_limit import R007


def test_r007(settle):
    result = settle([R007()], "r007.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R007"], ["R007"], [], []]
