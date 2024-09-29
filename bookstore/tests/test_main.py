import pytest
from fastapi import HTTPException
from datetime import timedelta
from bookstore.main import create_user_signup, login_for_access_token


@pytest.mark.asyncio
async def test_create_user_signup_success(mock_db, mock_pwd_context):
    user_credentials = {"email": "shashank@example.com", "password": "password"}
    response = await create_user_signup(user_credentials, db=mock_db)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert response["message"] == "User created successfully"


@pytest.mark.asyncio
async def test_create_user_signup_email_exists(mock_db, mock_pwd_context):
    mock_db.query().filter().first.return_value = {"email": "shashank@example.com", "password": "password"}
    user_credentials = {"email": "shashank@example.com", "password": "password"}
    with pytest.raises(HTTPException) as e:
        await create_user_signup(user_credentials, db=mock_db)
    assert e.value.status_code == 400
    assert e.value.detail == "Email already registered"

@pytest.mark.asyncio
async def test_login_success(mock_db, mock_pwd_context, mock_create_access_token):
    mock_db.query().filter().first.return_value = {"email": "shashank@example.com", "password": "hashed_password"}
    user_credentials = {"email": "shashank@example.com", "password": "password"}
    response = await login_for_access_token(user_credentials, db=mock_db)
    assert "access_token" in response
    assert response["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_failure(mock_db, mock_pwd_context, mock_create_access_token):
    mock_db.query().filter().first.return_value = None
    user_credentials = {"email": "shashank@example.com", "password": "password"}
    with pytest.raises(HTTPException) as e:
        await login_for_access_token(user_credentials, db=mock_db)
    assert e.value.status_code == 400
    assert e.value.detail == "Incorrect email or password"