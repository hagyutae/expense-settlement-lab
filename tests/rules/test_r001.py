from core.domain.rules.r001_required_fields import R001


def test_r001(settle):
    result = settle([R001()], "r001.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R001"], ["R001"], [], []]
