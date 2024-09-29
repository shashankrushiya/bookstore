import pytest
from unittest.mock import MagicMock, patch

from bookstore.database import get_db
from bookstore.middleware import JWTBearer
from bookstore.utils import create_access_token


@pytest.fixture
def mock_db():
    """Mocks the database session."""
    mock_session = MagicMock()
    with patch('database.get_db', return_value=mock_session):
        yield mock_session


@pytest.fixture
def mock_jwt():
    """Mocks the JWT functions."""
    with patch('middleware.jwt.decode', return_value={'sub': 'testuser'}):
        yield


@pytest.fixture
def mock_create_access_token():
    with patch('main.create_access_token', return_value="mocked_token"):
        yield


@pytest.fixture
def mock_pwd_context():
    """Mocks the password context."""
    mock_context = MagicMock()
    mock_context.hash.return_value = "hashed_password"
    mock_context.verify.return_value = True
    with patch('main.pwd_context', mock_context):
        yield mock_context
