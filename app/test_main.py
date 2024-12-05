import os

os.environ["DB_URL"] = "sqlite+aiosqlite://"

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.internal.db import DatabaseSessionManager

from .internal.models import Base

from .main import app

client = TestClient(app)

@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.anyio
async def test_save_imovel():
    session_manager = DatabaseSessionManager.create()
    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/imoveis/", json={"buyer": {"creditScore": 511, "estimatedIncome": 250_000}, "value": 110_000})
    assert response.status_code == 200
    body = response.json()
    assert body["id"] > 0

@pytest.mark.anyio
async def test_save_imovel_unprocessable_entity():
    session_manager = DatabaseSessionManager.create()
    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/imoveis/", json={"buyer": {"creditScore": -1, "estimatedIncome": 250_000}, "value": 110_000})
    assert response.status_code == 422

@pytest.mark.anyio
async def test_get_imovel():
    session_manager = DatabaseSessionManager.create()
    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create_res = await ac.post("/imoveis/", json={"buyer": {"creditScore": 511, "estimatedIncome": 250_000}, "value": 110_000})
        assert create_res.status_code == 200
        body = create_res.json()
        imovel_id = body["id"]
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/imoveis/{imovel_id}")
    
    assert response.status_code == 200
    assert response.json()["status"] != None

@pytest.mark.anyio
async def test_get_imovel_not_found():
    session_manager = DatabaseSessionManager.create()
    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/imoveis/9999")
    
    assert response.status_code == 404