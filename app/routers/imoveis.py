from typing import Annotated

from app.internal.dao import CreatePropertyRequest, CreatePropertyResponse, DealResponse
from app.internal.db import get_db_session
from app.internal.service.imoveis import save, find_by_id

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

router = APIRouter(
    prefix="/imoveis",
    tags=["imoveis"],
)

@router.post("/")
async def save_imovel(request: CreatePropertyRequest, db_session: DBSessionDep) -> CreatePropertyResponse:
    """
    Endpoint responsável por receber e criar as informações sobre o imovel e a negociação para persistência.
    Realiza a validação das informações e a avaliação de risco, retornando o ID da negociação criada
    """
    property = await save(db_session, request)
    return CreatePropertyResponse(id=property.id)

@router.get("/{imovel_id}", responses={
    404: {"detail": "Deal not found"}
})
async def get_imoveis(imovel_id: int, db_session: DBSessionDep) -> DealResponse:
    """
    Retorna uma negociação a partir do ID.
    """
    deal = await find_by_id(db_session, imovel_id)
    
    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    return deal