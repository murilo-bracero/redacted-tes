from typing import Annotated

from app.internal.dao import CreatePropertyRequest, CreatePropertyResponse
from app.internal.db import get_db_session
from app.internal.service.imoveis import save, find_by_id

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

router = APIRouter(
    prefix="/imoveis",
    tags=["imoveis"],
    responses={404: {"description": "Not found"}}
)

@router.post("")
async def save_imovel(request: CreatePropertyRequest, db_session: DBSessionDep):
    imovel = await save(db_session, request)
    return CreatePropertyResponse(id=imovel.id)

@router.get("/{imovel_id}")
async def get_imoveis(imovel_id: int, db_session: DBSessionDep):
    deal = await find_by_id(db_session, imovel_id)
    
    if deal is None:
        raise HTTPException(status_code=404, detail="Imovel not found")
    
    return deal