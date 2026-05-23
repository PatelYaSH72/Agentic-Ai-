import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ✅ Happy Path Tests

def test_signup_success():
    response = client.post("/auth/signup", json={
        "email": "newuser@gmail.com",
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_success():
    response = client.post("/auth/login", json={
        "email": "newuser@gmail.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_logout_success():
    # Pehle login karo token lene ke liye
    login = client.post("/auth/login", json={
        "email": "newuser@gmail.com",
        "password": "password123"
    })
    token = login.json()["access_token"]
    
    response = client.post(f"/auth/logout?token={token}")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"

# ❌ Error Path Tests

def test_signup_duplicate_email():
    # Same email dobara signup karo
    response = client.post("/auth/signup", json={
        "email": "newuser@gmail.com",
        "username": "anotheruser",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_wrong_password():
    response = client.post("/auth/login", json={
        "email": "newuser@gmail.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

def test_login_wrong_email():
    response = client.post("/auth/login", json={
        "email": "notexist@gmail.com",
        "password": "password123"
    })
    assert response.status_code == 401

def test_signup_invalid_email():
    response = client.post("/auth/signup", json={
        "email": "notanemail",
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 422