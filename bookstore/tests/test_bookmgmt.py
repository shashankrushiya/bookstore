import pytest
from fastapi import HTTPException
from bookstore.bookmgmt import create_book, update_book, delete_book, get_book_by_id, get_all_books


@pytest.mark.asyncio
async def test_create_book(mock_db):
    mock_book = {"name": "Shashank Book", "author": "Shashank Rushiya", "published_year": 2024, "book_summary": "Test Summary"}
    response = await create_book(mock_book, db=mock_db)
    mock_db.add.assert_called_once_with(mock_book)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert response == mock_book


@pytest.mark.asyncio
async def test_update_book(mock_db):
    mock_db.query().filter().first.return_value = {"id": 1, "name": "Old Book Name"}
    update_data = {"name": "New Book Name"}
    response = await update_book(1, update_data, db=mock_db)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert response["name"] == "New Book Name"


@pytest.mark.asyncio
async def test_update_book_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    update_data = {"name": "New Book Name"}
    with pytest.raises(HTTPException) as e:
        await update_book(1, update_data, db=mock_db)
    assert e.value.status_code == 404
    assert e.value.detail == "Book not found"


@pytest.mark.asyncio
async def test_delete_book(mock_db):
    mock_db.query().filter().first.return_value = {"id": 1}
    response = await delete_book(1, db=mock_db)
    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()
    assert response["message"] == "Book deleted successfully"


@pytest.mark.asyncio
async def test_delete_book_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as e:
        await delete_book(1, db=mock_db)
    assert e.value.status_code == 404
    assert e.value.detail == "Book not found"


@pytest.mark.asyncio
async def test_get_book_by_id(mock_db):
    mock_db.query().filter().first.return_value = {"id": 1, "name": "Test Book"}
    response = await get_book_by_id(1, db=mock_db)
    assert response["name"] == "Test Book"


@pytest.mark.asyncio
async def test_get_book_by_id_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as e:
        await get_book_by_id(1, db=mock_db)
    assert e.value.status_code == 404
    assert e.value.detail == "Book not found"


@pytest.mark.asyncio
async def test_get_all_books(mock_db):
    mock_db.query().all.return_value = [{"id": 1}, {"id": 2}]
    response = await get_all_books(db=mock_db)
    assert len(response) == 2

