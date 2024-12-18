from os import getenv

from contextlib import asynccontextmanager
from typing import Dict
from dotenv import load_dotenv

if getenv("ENV") != "prd":
    load_dotenv()

from fastapi import FastAPI

from app.internal.db import DatabaseSessionManager
from app.routers import imoveis

@asynccontextmanager
async def lifespan(_: FastAPI):
    yield 
    session_manager = DatabaseSessionManager.create()
    if session_manager.engine is not None:
        await session_manager.close()

# Ignoring lifespan type warning
app = FastAPI(lifespan=lifespan) # type: ignore

app.include_router(imoveis.router)

@app.get("/health", tags=["devops"])
async def health() -> Dict[str, str]:
    return {"status": "ok"}