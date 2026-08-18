from core.domain.rules.r006_meal_per_person import R006


def test_r006(settle):
    result = settle([R006()], "r006.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R006"], ["R006"], [], []]
