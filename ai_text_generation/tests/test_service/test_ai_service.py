from unittest.mock import patch
from app.services.ai_service import AIService, get_ai_provider
from app.services.ai_providers.openai_provider import OpenAIProvider


def test_get_ai_provider(monkeypatch):
    """Test `get_ai_provider` correctly returns an AI provider instance."""
    monkeypatch.setattr("app.config.Config.AI_MODEL_PROVIDER", "openai")

    provider = get_ai_provider()
    assert isinstance(provider, OpenAIProvider)


@patch("app.services.ai_service.get_ai_provider") 
def test_ai_service_get_response(mock_get_ai_provider):
    """Test AIService correctly calls the provider's get_response method."""
    mock_provider = mock_get_ai_provider.return_value
    mock_provider.get_response.return_value = "Mocked AI response"

    ai_service = AIService()
    
    response = ai_service.get_response("Hello, AI!")

    assert response == "Mocked AI response"

    mock_provider.get_response.assert_called_once_with("Hello, AI!")