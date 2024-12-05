MAX_PROPERTY_VALUE = 10_000_000
MIN_PROPERTY_VALUE = 100_000

MIN_CREDIT_SCORE = 500

DEAL_APPROVED = 'APROVADA'
DEAL_REJECTED = 'NEGADA'

def evaluate_risk(prop_value: float, credit_score: float, estimated_income: float)-> str:
    """
    @param prop_value: Valor do imovel
    @param credit_score: Credito do comprador
    @param estimated_income: Salário do comprador

    Avalia o risco e retorna se a negociação foi aprovada ou negada

    @return: Status da negociação
    """
    if prop_value > MAX_PROPERTY_VALUE or prop_value < MIN_PROPERTY_VALUE:
        return DEAL_REJECTED
    
    if credit_score < MIN_CREDIT_SCORE:
        return DEAL_REJECTED
    
    if prop_value > (estimated_income * 0.3):
        return DEAL_REJECTED

    return DEAL_APPROVED