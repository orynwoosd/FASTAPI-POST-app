from typing import List
from app import schemas

import pytest 

def test_get_all_posts(authorized_client, test_posts):

    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostVote(**post)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)

    assert res.status_code == 200


def test_unauthenticated_user_get_all_posts(client, test_posts):
    """An unauthenticated user tries getting all post"""
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthenticated_user_get_one_posts(client, test_posts):
    """Test unauthenticated user getting a specific post"""
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def get_one_post_not_existing(authorized_client, test_posts):
    """Test non existing post"""
    res = authorized_client.get("/posts/8888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    """Test authorized user gets a single post"""
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostVote(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "some true content", True),
    (" new guy", "SOme guy crazy", False),
    ("for new emperor", "content of truth", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts", json={"title": "title", "content": "content"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts", json={"title": "title", "content": "content"})

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}"
    )

    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}"
    )

    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        "/posts/45675"
    )

    assert res.status_code == 404

def test_delete_others_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[-1].id}"
    )

    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated Content",
        "id": test_posts[0].id
    }

    res =  authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    
def test_update_other_users_post(authorized_client, test_user, test_posts, test_user2):
    data = {
        "title": "Updated title",
        "content": "Updated Content",
        "id": test_posts[-1].id
    }

    res =  authorized_client.put(f"/posts/{test_posts[-1].id}", json=data)
    assert res.status_code == 403



def test_unauthorized_user_updates_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}", json={"title": "title", "content": "content"})

    assert res.status_code == 401



def test_update_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.put(
        "/posts/45675", json={"title": "title", "content": "content", "id": test_posts[0].id}
    )

    assert res.status_code == 404