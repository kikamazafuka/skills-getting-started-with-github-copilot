import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_read_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_activity():
    # Ensure the activity exists before testing
    activity_name = "Chess Club"
    email = "test@example.com"

    # Check if the activity exists
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert activity_name in activities

    # Test signing up for the activity
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code in [200, 400]  # 200 for success, 400 if already signed up
    assert "message" in response.json() or "detail" in response.json()


def test_unregister_activity():
    response = client.delete("/activities/sample_activity/unregister?email=test@example.com")
    assert response.status_code in [200, 404]  # 200 for success, 404 if not found
    assert "message" in response.json() or "detail" in response.json()