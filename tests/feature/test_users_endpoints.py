from fastapi import status


def test_create_user(client):
    payload = {
        "username": "testuseranother",
        "email": "testuseranother@example.com",
        "password": "test1password",
    }
    response = client.post("/api/users", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["data"]["username"] == "testuseranother"
    assert "email" in data["data"]


def test_read_users(client):
    response = client.get("/api/users")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data["data"], list)
    assert all("username" in user for user in data["data"])


def test_read_user(client):
    user_id = 1
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["data"]["id"] == user_id
    assert "username" in data["data"]


def test_update_user(client):
    user_id = 1
    payload = {
        "username": "updateduser",
        "email": "updateduser@example.com",
        "password": "updatedpassword",
    }
    response = client.put(f"/api/users/{user_id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["data"]["username"] == "updateduser"
    assert "email" in data["data"]


def test_delete_user(client):
    user_id = 1
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
