from core.domain.rules.r014_evidence_missing import R014


def test_r014(settle):
    result = settle([R014()], "r014.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R014"], ["R014"], [], []]
