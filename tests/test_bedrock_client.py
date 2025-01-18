import pytest
from bedrock_client import invoke_model_with_retry
from configs.models.amazon_titan_text_express_v1 import model_id, token_limit


model_id, token_limit

def test_invoke_model_with_retry(monkeypatch):
    def mock_invoke_model_with_retry(model_id, data):
        return "mocked result"
    
    monkeypatch.setattr("bedrock_client.invoke_model_with_retry", mock_invoke_model_with_retry)
    
    result = invoke_model_with_retry(model_id, "test data")
    assert result == "mocked result"

def test_invoke_model_with_retry_failure(monkeypatch):
    def mock_invoke_model_with_retry(model_id, data):
        raise RuntimeError("Test exception")
    
    monkeypatch.setattr("bedrock_client.invoke_model_with_retry", mock_invoke_model_with_retry)
    
    with pytest.raises(RuntimeError, match="Test exception"):
        invoke_model_with_retry(model_id, "test data", retries=1)