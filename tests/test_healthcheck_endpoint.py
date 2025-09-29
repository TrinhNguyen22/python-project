# import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_healthcheck_endpoint_should_response_ok():
    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        'status': 'OK',
        'message': 'API services is up and running'
    }