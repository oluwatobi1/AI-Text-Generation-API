import pytest
from app.models import User, GeneratedText


def test_generated_text_model(db_session, test_user):
    """
    Ensure the GeneratedText model stores and retrieves data correctly.
    """
    text = GeneratedText(user_id=test_user.id, prompt="Hello AI Model", response="Hi!")
    db_session.add(text)
    db_session.commit()

    retrieved_text = GeneratedText.query.first()
    assert retrieved_text is not None
    assert retrieved_text.prompt == "Hello AI Model"
    assert retrieved_text.response == "Hi!"
    assert retrieved_text.user_id == test_user.id


def test_user_model(db_session):
    """
    Ensure the User model stores and retrieves data correctly
    """
    user =User(username="test_user")
    user.set_password("password")
    db_session.add(user)
    db_session.commit()

    retrieved_user = User.query.first()
    assert retrieved_user is not None
    assert retrieved_user.username == "test_user"
    assert retrieved_user.check_password("password")


password_test_cases = [
    pytest.param("password", "password", True, id="PASSWORD:VALID_PASSWORD"),
    pytest.param("password", "wrong_password", False, id="PASSWORD:WRONG_PASSWORD"),
]

@pytest.mark.parametrize("password, check_password, expected_value", password_test_cases)
def test_password_hashing(password, check_password, expected_value):
    """
    Test password hashing and checking
    """
    user = User(username="test_user")
    user.set_password(password)
    assert user.check_password(check_password) == expected_value