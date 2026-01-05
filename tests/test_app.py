import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Programming Class/signup?email=duplicate@mergington.edu")
    # Second should fail
    response = client.post("/activities/Programming Class/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404

def test_delete_success():
    # Signup first
    client.post("/activities/Basketball/signup?email=deletetest@mergington.edu")
    # Then delete
    response = client.delete("/activities/Basketball/signup?email=deletetest@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]

def test_delete_not_signed_up():
    response = client.delete("/activities/Tennis Club/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"]

def test_delete_invalid_activity():
    response = client.delete("/activities/Invalid Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404

def test_root_redirect():
    response = client.get("/", allow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert "/static/index.html" in response.headers["location"]