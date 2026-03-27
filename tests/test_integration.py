import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_task():
    client.post("/auth/register", json={"username": "testuser", "password": "123456"})
    login = client.post("/auth/login", json={"username": "testuser", "password": "123456"})
    token = login.json()["access_token"]

    response = client.post(
        "/v1/tasks/",
        json={"title": "Интеграционный тест", "is_done": False},
        headers={"Authorization": token},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Интеграционный тест"