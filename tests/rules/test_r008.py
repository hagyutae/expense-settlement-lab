from core.domain.rules.r008_transport_limit import R008


def test_r008(settle):
    result = settle([R008()], "r008.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R008"], ["R008"], [], []]
