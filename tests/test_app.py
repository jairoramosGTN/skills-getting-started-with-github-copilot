import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_duplicate():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Find index
    idx = None
    if email in activities[activity]["participants"]:
        idx = activities[activity]["participants"].index(email)
    else:
        activities[activity]["participants"].append(email)
        idx = activities[activity]["participants"].index(email)
    response = client.post(f"/activities/{activity}/unregister", json={"index": idx})
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_invalid_index():
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/unregister", json={"index": 999})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid participant index"


def test_unregister_invalid_activity():
    response = client.post(f"/activities/Nonexistent/unregister", json={"index": 0})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
