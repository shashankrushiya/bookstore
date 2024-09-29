import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.orm import Session
import os
from bookstore.database import engine, Base, UserCredentials, Book
from bookstore.main import app
import jwt


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_signup(client, test_db):
    response = await client.post("/signup", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


@pytest.mark.asyncio
async def test_login(client, test_db):
    await client.post("/signup", json={"email": "test@example.com", "password": "password"})
    response = await client.post("/login", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_create_book(client, test_db):
    await client.post("/signup", json={"email": "test@example.com", "password": "password"})
    login_response = await client.post("/login", json={"email": "test@example.com", "password": "password"})
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    book_data = {"name": "Test Book", "author": "Test Author", "published_year": 2024, "book_summary": "Test Summary"}
    response = await client.post("/books/", json=book_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Book"


@pytest.mark.asyncio
async def test_get_book(client, test_db):
    await client.post("/signup", json={"email": "test@example.com", "password": "password"})
    login_response = await client.post("/login", json={"email": "test@example.com", "password": "password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    book_data = {"name": "Test Book", "author": "Test Author", "published_year": 2024, "book_summary": "Test Summary"}
    create_response = await client.post("/books/", json=book_data, headers=headers)
    book_id = create_response.json()["id"]

    response = await client.get(f"/books/{book_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Book"


@pytest.mark.asyncio
async def test_update_book(client, test_db):
    await client.post("/signup", json={"email": "test@example.com", "password": "password"})
    login_response = await client.post("/login", json={"email": "test@example.com", "password": "password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    book_data = {"name": "Test Book", "author": "Test Author", "published_year": 2024, "book_summary": "Test Summary"}
    create_response = await client.post("/books/", json=book_data, headers=headers)
    book_id = create_response.json()["id"]

    update_data = {"name": "Updated Book Name"}
    response = await client.put(f"/books/{book_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Book Name"


@pytest.mark.asyncio
async def test_delete_book(client, test_db):
    await client.post("/signup", json={"email": "test@example.com", "password": "password"})
    login_response = await client.post("/login", json={"email": "test@example.com", "password": "password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    book_data = {"name": "Test Book", "author": "Test Author", "published_year": 2024, "book_summary": "Test Summary"}
    create_response = await client.post("/books/", json=book_data, headers=headers)
    book_id = create_response.json()["id"]

    response = await client.delete(f"/books/{book_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"

