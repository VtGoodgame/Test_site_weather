from httpx import AsyncClient,  ASGITransport
import pytest 
from backend.main import app

@pytest.mark.asyncio
async def test_main_page():
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        transport=ASGITransport(app=app)) as client:
        response = await client.get("/Moscow")
        print(response)
        assert response.status_code != 200

@pytest.mark.asyncio
async def test_forecast():
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        transport=ASGITransport(app=app)) as client:
        response = await client.get("/forecast/Moscow")
        print(response)
        assert response.status_code != 200