from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.dao import CreatePropertyRequest, DealBuyerResponse, DealPropertyResponse, DealResponse
from app.internal.models import Comprador, Imovel, Negociacao

MAX_PROPERTY_VALUE = 10_000_000
MIN_PROPERTY_VALUE = 100_000

MIN_CREDIT_SCORE = 500

DEAL_APPROVED = 'APROVADA'
DEAL_REJECTED = 'NEGADA'

async def save(db_session: AsyncSession, request: CreatePropertyRequest)-> Negociacao:
    comprador = Comprador(
        nome=request.buyer.name,
        historico_credito=request.buyer.credit_score,
        renda_estimada=request.buyer.wage
    )
    
    imovel = Imovel(
        valor=request.value,
        cep=request.zip_code,
        numero=request.number,
        logradouro='abc 2',
    )

    negociacao = Negociacao()

    negociacao.status = _evaluate_deal(imovel.valor, comprador.historico_credito, comprador.renda_estimada)

    negociacao.comprador = comprador
    negociacao.imovel = imovel

    db_session.add(negociacao)
    await db_session.commit()
    await db_session.refresh(negociacao)
    return negociacao

async def find_by_id(db_session: AsyncSession, negociacao_id: int)-> Optional[DealResponse]:
    entity = await db_session.get(Negociacao, negociacao_id)

    if entity is None:
        return None

    return DealResponse(
        id=entity.id,
        status=entity.status,
        buyer=DealBuyerResponse(
            id=entity.comprador.id,
            nome=entity.comprador.nome,
            credit_score=entity.comprador.historico_credito,
            wage=entity.comprador.renda_estimada
        ),
        property=DealPropertyResponse(
            id=entity.imovel.id,
            zip_code=entity.imovel.cep,
            number=entity.imovel.numero,
            value=entity.imovel.valor,
            public_place=entity.imovel.logradouro
        )
    )

def _evaluate_deal(prop_value: float, credit_score: float, wage: float)-> str:
    if prop_value > MAX_PROPERTY_VALUE or prop_value < MIN_PROPERTY_VALUE:
        return DEAL_REJECTED
    
    if credit_score < MIN_CREDIT_SCORE:
        return DEAL_REJECTED
    
    if prop_value > (wage * 0.3):
        return DEAL_REJECTED

    return DEAL_APPROVED
