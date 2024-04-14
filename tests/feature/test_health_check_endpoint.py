from fastapi import status


def test_health_check(client):
    response = client.get("/api/health-check")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "message": "OK",
        "status_code": 200,
    }
