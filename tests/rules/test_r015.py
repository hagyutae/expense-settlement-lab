from core.domain.rules.r015_category_merchant import R015


def test_r015(settle):
    result = settle([R015()], "r015.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R015"], ["R015"], [], []]
