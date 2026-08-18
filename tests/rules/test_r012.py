from core.domain.rules.r012_entertainment_per_person import R012


def test_r012(settle):
    result = settle([R012()], "r012.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R012"], ["R012"], [], []]
