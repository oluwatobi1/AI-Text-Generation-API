from app.models import GeneratedText
from app.repositories.generated_text_repository import GeneratedTextRepository


def test_create_generated_text(db_session, test_user):
    """Test creating a generated text entry."""
    prompt = "What is AI?"
    response = "AI stands for Artificial Intelligence."

    generated_text = GeneratedTextRepository.create_generated_text(
        user_id=test_user.id, prompt=prompt, response=response
    )

    assert generated_text is not None
    assert generated_text.user_id == test_user.id
    assert generated_text.prompt == prompt
    assert generated_text.response == response

    # Check if saved in DB
    db_text = db_session.query(GeneratedText).filter_by(id=generated_text.id).first()
    assert db_text is not None
    assert db_text.prompt == prompt


def test_get_user_generated_texts_by_id(db_session, test_user):
    """Test retrieving a user's generated text by ID."""
    generated_text = GeneratedTextRepository.create_generated_text(
        user_id=test_user.id, prompt="Hello?", response="Hi there!"
    )

    retrieved_text = GeneratedTextRepository.get_user_generated_texts_by_id(
        id=generated_text.id, user_id=test_user.id
    )
    assert retrieved_text is not None
    assert retrieved_text.id == generated_text.id
    assert retrieved_text.response == "Hi there!"


def test_delete_generated_text(db_session, test_user):
    """Test deleting a generated text."""
    generated_text = GeneratedTextRepository.create_generated_text(
        user_id=test_user.id, prompt="Delete me?", response="Sure!"
    )
    assert db_session.query(GeneratedText).filter_by(id=generated_text.id).first() is not None

    result = GeneratedTextRepository.delete_generated_text(generated_text)

    assert result is True
    assert db_session.query(GeneratedText).filter_by(id=generated_text.id).first() is None


def test_update_generated_text(db_session, test_user):
    """Test updating a generated text response."""
    generated_text = GeneratedTextRepository.create_generated_text(
        user_id=test_user.id, prompt="Old prompt", response="Old response"
    )

    generated_text.prompt = "Updated prompt"
    generated_text.response = "Updated response"

    updated_text = GeneratedTextRepository.update_generated_text(generated_text)

    assert updated_text is not None
    assert updated_text.prompt == "Updated prompt"
    assert updated_text.response == "Updated response"
