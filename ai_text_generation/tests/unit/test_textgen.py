import pytest
from app import db
from app.models import GeneratedText
from unittest.mock import patch
from flask import url_for


@pytest.fixture
def sample_text(db_session, test_user):
    text = GeneratedText(id="ceb6ddebd6d7494c9449c144ff256141", prompt="sample prompt", user_id=test_user.id, response="sample response")
    
    db_session.add(text)
    db_session.commit()
    return text

# Test cases for text generation
generate_text_test_cases = [
    pytest.param({"prompt": "Tell me a joke"}, 201, "Here’s a funny joke!", id="CREATE:VALID_TEXT_GENERATION"),
    pytest.param({"prompt": ""}, 422, None, id="CREATE:EMPTY_PROMPT"),
    pytest.param(None, 401, None, id="CREATE:UNAUTHORIZED"),
]

@pytest.mark.parametrize("input_data, expected_status, mock_response", generate_text_test_cases)
@patch("app.services.ai_service.ai_service.get_response")
def test_generate_text(mock_ai_service, client, auth_header, input_data, expected_status, mock_response):
    """
    Test create/text generation with AI service mocked
    """
    mock_ai_service.return_value = mock_response
    with  client.application.test_request_context():
        url = url_for("textgen.TextGenResource")
        header = auth_header if input_data else {}
        response = client.post(url, json=input_data, headers= header)
        assert response.status_code == expected_status
        if expected_status == 201:
            assert response.json.get("response") == mock_response

    
# Test cases for updating prompt
update_prompt_test_cases = [
    pytest.param("ceb6ddebd6d7494c9449c144ff256141", {"prompt": "updated the prompt"}, 200, "updated AI response", id="UPDATE:VALID_TEXT_GENERATION"),
    pytest.param("non_existent_text_id", {"prompt": "again the prompt"}, 404, None, id="UPDATE:NON_EXISTENT_TEXT"),
    pytest.param("rand", None, 401, None, id="UPDATE:UNAUTHORIZED"),
]

@pytest.mark.parametrize("text_id, input_data, expected_status, mock_response", update_prompt_test_cases)
@patch("app.services.ai_service.ai_service.get_response")
def test_update_prompt(mock_ai_service, client, auth_header,sample_text, text_id, input_data, expected_status, mock_response):
    """
    Test updating prompt with AI service mocked
    """
    mock_ai_service.return_value = mock_response # Mock  AI response
    with client.application.test_request_context():
        url = url_for("textgen.TextGenByIdResource", id=text_id)
        
        header = auth_header if input_data else {}
        response  = client.put(url, json=input_data, headers=header)
        assert response.status_code == expected_status
        if expected_status == 200:
            assert response.json.get("response") == mock_response
            assert GeneratedText.query.get(text_id).prompt == input_data.get("prompt")


# Test cases for deleting text
delete_text_test_cases = [
    pytest.param("ceb6ddebd6d7494c9449c144ff256141", 200, True, id="DELETE:VALID_TEXT_GENERATION"),
    pytest.param("non_existent_text_id", 404, True, id="DELETE:NON_EXISTENT_TEXT"),
    pytest.param("unauthorized_request", 401, False, id="DELETE:UNAUTHORIZED"),
]

@pytest.mark.parametrize("text_id, expected_status, is_authenticated", delete_text_test_cases)
def test_delete_text(client, auth_header, sample_text, text_id, expected_status, is_authenticated):
    """
    Test delete text
    """
    with client.application.test_request_context():
        url = url_for("textgen.TextGenByIdResource", id=text_id)
        header = auth_header if is_authenticated else {}
        response = client.delete(url, headers=header)
        assert response.status_code == expected_status
        if expected_status == 200:
            assert GeneratedText.query.get(text_id) is None

# Test cases for retrieving text
get_text_test_cases = [
    pytest.param("ceb6ddebd6d7494c9449c144ff256141", 200, True, id="GET:VALID_TEXT_GENERATION"),
    pytest.param("non_existent_text_id", 404, True, id="GET:NON_EXISTENT_TEXT"),
    pytest.param("unauthorized_request", 401, False, id="GET:UNAUTHORIZED"),
]

@pytest.mark.parametrize("text_id, expected_status, is_authenticated", get_text_test_cases)
def test_get_text(client, auth_header, sample_text, text_id, expected_status, is_authenticated):
    """
        Test retrieving generated text
    """
    with client.application.test_request_context():
        url = url_for("textgen.TextGenByIdResource", id=text_id)
        header = auth_header if is_authenticated else {}
        response = client.get(url, headers=header)
        assert response.status_code == expected_status
        if expected_status == 200:
            assert response.json.get("response") == sample_text.response
            assert response.json.get("prompt") == sample_text.prompt