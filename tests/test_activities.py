def test_get_all_activities(client):
    # Arrange (client fixture provides TestClient and snapshot restores state)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    for details in data.values():
        assert 'description' in details
        assert 'schedule' in details
        assert 'max_participants' in details
        assert 'participants' in details


def test_signup_success(client):
    # Arrange
    resp = client.get("/activities")
    activities = resp.json()
    activity = list(activities.keys())[0]
    email = "test_student@example.com"

    # Act
    signup = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert signup.status_code == 200
    body = signup.json()
    assert 'message' in body and isinstance(body['message'], str)

    # Verify the participants list was updated
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]['participants']


def test_signup_nonexistent_activity(client):
    # Arrange
    email = "nobody@example.com"

    # Act
    resp = client.post(f"/activities/this-activity-does-not-exist/signup?email={email}")

    # Assert
    assert resp.status_code == 404


def test_signup_duplicate_email(client):
    # Arrange
    resp = client.get("/activities")
    activity = list(resp.json().keys())[0]
    email = "duplicate@example.com"
    first = client.post(f"/activities/{activity}/signup?email={email}")
    assert first.status_code == 200

    # Act: attempt duplicate signup
    second = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert second.status_code == 400
