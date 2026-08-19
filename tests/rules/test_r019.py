from core.domain.rules.r019_department_monthly_limit import R019


def test_r019(settle):
    result = settle([R019()], "r019.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [[], [], ["R019"], ["R019"]]
