from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.dao import CreatePropertyRequest, DealBuyerResponse, DealPropertyResponse, DealResponse
from app.internal.models import Buyer, Deal, Property

MAX_PROPERTY_VALUE = 10_000_000
MIN_PROPERTY_VALUE = 100_000

MIN_CREDIT_SCORE = 500

DEAL_APPROVED = 'APROVADA'
DEAL_REJECTED = 'NEGADA'

async def save(db_session: AsyncSession, request: CreatePropertyRequest) -> Deal:
    """
    @param db_session: Sessão assíncrona do banco de dados
    @param request: Requisição de criação de imovel

    Realiza a avaliação de risco e salva a negociação, o imovel
    e o comprador no banco de dados.

    @return: Negociação
    """
    buyer = Buyer(
        credit_score=request.buyer.credit_score,
        estimated_income=request.buyer.estimated_income
    )
    
    property = Property(
        value = request.value
    )

    deal = Deal()

    deal.status = _evaluate_risk(property.value, buyer.credit_score, buyer.estimated_income)

    deal.buyer = buyer
    deal.property = property

    db_session.add(deal)
    await db_session.commit()
    await db_session.refresh(deal)
    return deal

async def find_by_id(db_session: AsyncSession, deal_id: int)-> Optional[DealResponse]:
    """
    @param db_session: Sessão assíncrona do banco de dados
    @param deal_id: ID da negociação

    @return: Opcional da negociação, se ela for encontrada
    """
    entity = await db_session.get(Deal, deal_id)

    if entity is None:
        return None

    return DealResponse(
        id=entity.id,
        status=entity.status,
        buyer=DealBuyerResponse(
            id=entity.buyer.id,
            credit_score=entity.buyer.credit_score,
            estimated_income=entity.buyer.estimated_income
        ),
        property=DealPropertyResponse(
            id=entity.buyer.id,
            value=entity.property.value,
        )
    )

def _evaluate_risk(prop_value: float, credit_score: float, estimated_income: float)-> str:
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
