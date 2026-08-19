from core.domain.rules.r020_daily_meal_duplicated import R020


def test_r020(settle):
    result = settle([R020()], "r020.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R020"], ["R020"], [], []]
