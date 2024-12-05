from .risk_evaluation import evaluate_risk, MAX_PROPERTY_VALUE, MIN_PROPERTY_VALUE

def test_evaluate_risk_happy_path():
    res = evaluate_risk(105_000, 701, 350_000)

    assert res == "APROVADA"

def test_evaluate_risk_credit():
    res = evaluate_risk(150_000, 499, 250_000)

    assert res == "NEGADA"

def test_evaluate_risk_property_value_max():
    res = evaluate_risk(MAX_PROPERTY_VALUE, 700, 250_000)

    assert res == "NEGADA"

def test_evaluate_risk_property_value_min():
    res = evaluate_risk(MIN_PROPERTY_VALUE, 700, 250_000)

    assert res == "NEGADA"

def test_evaluate_risk_estimated_income():
    estimated_income = 250_000
    prop_value = (estimated_income * 0.3) + 1

    res = evaluate_risk(prop_value, 700, estimated_income)

    assert res == "NEGADA"
