from core.domain.rules.r017_claim_duplicated import R017


def test_r017(settle):
    result = settle([R017()], "r017.csv")
    codes = [[v.code for v in j.violations] for j in result.judgements]
    assert codes == [["R017"], ["R017"], [], []]
