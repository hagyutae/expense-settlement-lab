from core.domain.rules.r016_personal_card_reason import R016


def test_r016(settle):
    result = settle([R016()], "r016.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R016"], ["R016"], [], []]
