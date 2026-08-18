from core.domain.rules.r011_entertainment_attendees import R011


def test_r011(settle):
    result = settle([R011()], "r011.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R011"], ["R011"], [], []]
