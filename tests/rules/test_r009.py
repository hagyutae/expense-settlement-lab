from core.domain.rules.r009_payment_method import R009


def test_r009(settle):
    result = settle([R009()], "r009.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R009"], ["R009"], [], []]
