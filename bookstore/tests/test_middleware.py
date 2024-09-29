from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from bookstore.middleware import JWTBearer


def test_verify_jwt_valid_token(monkeypatch):
    monkeypatch.setattr("middleware.jwt.decode", lambda token, key, algorithms: {"sub": "testuser"})
    bearer = JWTBearer()
    assert bearer.verify_jwt("test_token") is True


def test_verify_jwt_invalid_token(monkeypatch):
    monkeypatch.setattr("middleware.jwt.decode", lambda token, key, algorithms: None)
    bearer = JWTBearer()
    assert bearer.verify_jwt("test_token") is True


@pytest.mark.asyncio
async def test_jwt_bearer_valid_token(mock_jwt):
    bearer = JWTBearer()
    mock_request = MagicMock()
    mock_request.headers = {"Authorization": "Bearer test_token"}
    credentials = await bearer(mock_request)
    assert credentials == "test_token"


@pytest.mark.asyncio
async def test_jwt_bearer_invalid_token(mock_jwt):
    bearer = JWTBearer()
    mock_request = MagicMock()
    mock_request.headers = {"Authorization": "Bearer invalid_token"}
    with pytest.raises(HTTPException) as e:
        await bearer(mock_request)
    assert e.value.status_code == 403
    assert e.value.detail == "Invalid token or expired token"


@pytest.mark.asyncio
async def test_jwt_bearer_no_token():
    bearer = JWTBearer()
    mock_request = MagicMock()
    mock_request.headers = {}
    with pytest.raises(HTTPException) as e:
        await bearer(mock_request)
    assert e.value.status_code == 403
    assert e.value.detail == "Invalid authorization code."
