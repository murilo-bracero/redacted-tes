from os import getenv

from contextlib import asynccontextmanager
from dotenv import load_dotenv

if getenv("ENV") != "prd":
    load_dotenv()

from fastapi import FastAPI

from app.internal.db import session_manager
from app.routers import imoveis

@asynccontextmanager
async def lifespan(_: FastAPI):
    yield 
    if session_manager.engine is not None:
        await session_manager.close()

# Ignoring lifespan type warning
app = FastAPI(lifespan=lifespan) # type: ignore

app.include_router(imoveis.router)

@app.get("/health")
async def health():
    return {"status": "ok"}