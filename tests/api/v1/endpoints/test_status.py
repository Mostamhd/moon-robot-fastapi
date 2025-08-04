# test_status.py
import pytest


@pytest.mark.asyncio
async def test_get_status_initial(client):
    response = await client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == {"x": 0, "y": 0}
    assert data["direction"] == "NORTH"


@pytest.mark.asyncio
async def test_get_status_after_commands(client):
    await client.post("/api/v1/commands", json={"command": "FF"})
    response = await client.get("/api/v1/status")
    data = response.json()
    assert data["position"] == {"x": 0, "y": 2}
    assert data["direction"] == "NORTH"


@pytest.mark.asyncio
async def test_get_status_with_rotation(client):
    await client.post("/api/v1/commands", json={"command": "RFL"})
    response = await client.get("/api/v1/status")
    data = response.json()
    assert data["position"] == {"x": 1, "y": 0}
    assert data["direction"] == "NORTH"


@pytest.mark.asyncio
async def test_get_status_with_invalid_commands(client):
    await client.post("/api/v1/commands", json={"command": "HAHA"})
    response = await client.get("/api/v1/status")
    data = response.json()
    assert data["position"] == {"x": 0, "y": 0}
    assert data["direction"] == "NORTH"
