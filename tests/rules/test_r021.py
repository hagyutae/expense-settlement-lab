from core.domain.rules.r021_training_preapproval import R021


def test_r021(settle):
    result = settle([R021()], "r021.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R021"], ["R021"], [], []]
