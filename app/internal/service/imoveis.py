from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.dao import CreatePropertyRequest, DealBuyerResponse, DealPropertyResponse, DealResponse
from app.internal.models import Buyer, Deal, Property
from .risk_evaluation import evaluate_risk

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

    deal.status = evaluate_risk(property.value, buyer.credit_score, buyer.estimated_income)

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
