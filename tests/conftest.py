
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.oauth2 import create_access_token
from app.database import SessionLocal



@pytest.fixture()
def client():
    # command.upgrade("head")
    # Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # command.downgrade("base")
    # Base.metadata.drop_all(bind=engine)



@pytest.fixture
def test_user(client):
    user_data = {"email": "abc@xyz.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "def@xyz.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture()
def test_posts(test_user,test_user2):
    posts_data = [
        {"title": "first title", "content": "first content", "owner_id": test_user["id"]},
        {"title": "second title", "content": "second content", "owner_id": test_user["id"]},
        {"title": "third title", "content": "third content", "owner_id": test_user2["id"]},
    ]

    def create_post_model(post):
        return app.models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    db = SessionLocal()
    db.add_all(posts)
    db.commit()
    return db.query(app.models.Post).all()