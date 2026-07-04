from app import schemas
from jose import jwt
from app.config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

# def test_root(client):
#     res=client.get("/")
#     print(res.json())
#     assert res.json().get("message")=="Welcome to the API"
#     assert res.status_code==200

# def test_create_user(client):
#     res = client.post("/users/", json={"email": "example@example.com", "password": "password123"})
#     new_user = schemas.UserOut(**res.json())
#     assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id: str = payload.get("user_id")
    assert res.status_code == 200

def test_incorrect_login(client):
    res = client.post("/login", data={"username": "incorrect@example.com", "password": "wrongpassword"})
    assert res.status_code == 401