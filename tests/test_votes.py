def test_vote_on_post(authorized_client,test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice_on_post(authorized_client,test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 409

def test_delete_vote_on_post(authorized_client,test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 201

def test_delete_vote_on_post_not_exist(authorized_client,test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 888888, "dir": 0})
    assert res.status_code == 404

def test_vote_on_post_not_exist(authorized_client,test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 888888, "dir": 1})
    assert res.status_code == 404

def test_delete_vote_on_post_not_voted(authorized_client,test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 404

def test_unauthorized_user_vote_on_post(client,test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401

def test_unauthorized_user_delete_vote_on_post(client,test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 401
