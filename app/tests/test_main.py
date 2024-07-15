from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_shorten_url():
    response = client.post("/shorten", json={"url": "http://example.com", "expires_at": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat()})
    assert response.status_code == 200
    assert "short_url" in response.json()

def test_redirect_url():
    response = client.post("/shorten", json={"url": "http://example.com", "expires_at": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat()})
    assert response.status_code == 200
    short_url = response.json().get("short_url")
    assert short_url is not None
    
    response = client.get(f"/{short_url}")
    assert response.status_code == 301
    assert response.headers["location"] == "http://example.com"

def test_get_stats():
    response = client.post("/shorten", json={"url": "http://example.com", "expires_at": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat()})
    assert response.status_code == 200
    short_url = response.json().get("short_url")
    assert short_url is not None
    
    response = client.get(f"/stats/{short_url}")
    assert response.status_code == 200
    assert response.json()["visit_count"] == 0
    
    client.get(f"/{short_url}")
    
    response = client.get(f"/stats/{short_url}")
    assert response.status_code == 200
    assert response.json()["visit_count"] == 1
