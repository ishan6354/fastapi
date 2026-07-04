from app.schemas import  Post


def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client,test_posts): 
    res = client.get("/posts/")
    assert res.status_code == 401      


def test_unauthorized_user_get_one_post(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/888888")
    assert res.status_code == 404


def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200


def test_create_post(authorized_client,test_user):      
    res = authorized_client.post("/posts/",json={"title":"test title","content":"test content","published":False})
    created_post = Post(**res.json())
    assert res.status_code == 201
   

def test_unauthorized_user_create_post(client,test_user):
    res = client.post("/posts/",json={"title":"test title","content":"test content","published":False})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/888888")
    assert res.status_code == 404


def test_delete_post_non_owner(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403


def test_update_post(authorized_client,test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}",json=data)
    updated_post = Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_post_non_exist(authorized_client,test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/888888",json=data)
    assert res.status_code == 404


def test_update_post_non_owner(authorized_client,test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[2].id
    }
    res = authorized_client.put(f"/posts/{test_posts[2].id}",json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client,test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}",json=data)
    assert res.status_code == 401