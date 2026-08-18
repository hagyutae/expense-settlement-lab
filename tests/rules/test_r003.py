from core.domain.rules.r003_date_reversed import R003


def test_r003(settle):
    result = settle([R003()], "r003.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R003"], ["R003"], [], []]
