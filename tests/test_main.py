from fastapi.testclient import TestClient
from main import app, ModelRequest

client = TestClient(app)

def test_invoke_model_success(monkeypatch):
    def mock_invoke_model_with_retry(model_id, body):
        return "mocked result"
    
    monkeypatch.setattr("main.invoke_model_with_retry", mock_invoke_model_with_retry)
    
    response = client.post("/invoke_model", json={"model_id": "test_model", "body": "test body"})
    assert response.status_code == 200
    assert response.json() == {"result": "mocked result"}

def test_invoke_model_failure(monkeypatch):
    def mock_invoke_model_with_retry(model_id, body):
        return None
    
    monkeypatch.setattr("main.invoke_model_with_retry", mock_invoke_model_with_retry)
    
    response = client.post("/invoke_model", json={"model_id": "test_model", "body": "test body"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Model invocation failed"}

def test_invoke_model_exception(monkeypatch):
    def mock_invoke_model_with_retry(model_id, body):
        raise Exception("Test exception")
    
    monkeypatch.setattr("main.invoke_model_with_retry", mock_invoke_model_with_retry)
    
    response = client.post("/invoke_model", json={"model_id": "test_model", "body": "test body"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Test exception"}