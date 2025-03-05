from app.models import User
from app.repositories.user_repository import UserRepository


def test_create_user(db_session):
    """Test creating a user."""
    username = "test_user"
    password = "secure_password"

    user = UserRepository.create_user(username=username, password=password)

    assert user is not None
    assert user.username == username
    assert user.check_password(password)  

    # Check if saved in DB
    db_user = db_session.query(User).filter_by(username=username).first()
    assert db_user is not None
    assert db_user.username == username


def test_get_user_by_username(test_user):
    """Test retrieving a user by username."""
    retrieved_user = UserRepository.get_user_by_username(test_user.username)

    assert retrieved_user is not None
    assert retrieved_user.username == test_user.username
    assert retrieved_user.id == test_user.id


def test_get_user_by_id(test_user):
    """Test retrieving a user by ID."""
    retrieved_user = UserRepository.get_user_by_id(test_user.id)

    assert retrieved_user is not None
    assert retrieved_user.id == test_user.id
    assert retrieved_user.username == test_user.username
