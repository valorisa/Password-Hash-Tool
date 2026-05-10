from fastapi.testclient import TestClient

from password_hash_tool.api import app

client = TestClient(app)


def test_hash_endpoint():
    response = client.post("/hash", json={"password": "testpassword", "algorithm": "bcrypt"})
    assert response.status_code == 200
    data = response.json()
    assert data["algorithm"] == "bcrypt"
    assert "$2b$" in data["hash"]


def test_verify_endpoint():
    hash_resp = client.post("/hash", json={"password": "testpassword", "algorithm": "argon2id"})
    hash_value = hash_resp.json()["hash"]

    response = client.post("/verify", json={"password": "testpassword", "hash": hash_value})
    assert response.status_code == 200
    assert response.json()["valid"] is True

    response = client.post("/verify", json={"password": "wrong", "hash": hash_value})
    assert response.status_code == 200
    assert response.json()["valid"] is False


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hash_invalid_algorithm():
    response = client.post("/hash", json={"password": "test", "algorithm": "md5"})
    assert response.status_code == 400


def test_verify_unknown_format():
    response = client.post("/verify", json={"password": "test", "hash": "not-a-valid-hash"})
    assert response.status_code == 400
