from fastapi.testclient import TestClient
from app.main import app
from app.model import Post

client = TestClient(app)

dummy_post: Post = {
    "title": "Deneme",
    "short_description": "yeni tarih",
    "description": "deneme description lorem aloo asda asdas",
    "tags": ["deneme", "#hashtag", "arama"],
}

wrong_dummy_post: Post = {
    "title": "Deneme",
    "short_description": "yeni tarih",
    "content": "deneme description lorem aloo asda asdas",
    "tags": ["deneme", "#hashtag", "arama"],
}


def test_home_without_data():
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.json() == []


def test_insert_data():
    response = client.post(
        "/posts",
        json=dummy_post,
    )
    post: Post = response.json()

    assert response.status_code == 201
    assert post["title"] == dummy_post["title"]
    assert post["short_description"] == dummy_post["short_description"]
    assert post["description"] == dummy_post["description"]
    assert post["tags"] == dummy_post["tags"]


def test_insert_data_wrong_format():
    response = client.post(
        "/posts",
        json=wrong_dummy_post,
    )
    post: Post = response.json()

    assert response.status_code == 422
    assert post["field"] == "description"
    assert post["msg"] == "Field required"


def test_home_with_data():
    response = client.get("/posts")
    post: Post = response.json()

    assert response.status_code == 200
    assert type(post) == list
    assert post[0]["title"] == dummy_post["title"]
    assert post[0]["short_description"] == dummy_post["short_description"]
    assert post[0]["description"] == dummy_post["description"]
    assert post[0]["tags"] == dummy_post["tags"]


def test_get_data():
    response = client.get("/posts/Deneme")
    post: Post = response.json()

    assert response.status_code == 200
    assert post["title"] == dummy_post["title"]
    assert post["short_description"] == dummy_post["short_description"]
    assert post["description"] == dummy_post["description"]
    assert post["tags"] == dummy_post["tags"]


def test_delete_data():
    response = client.delete("/posts/Deneme")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Post with title 'Deneme' deleted successfully"
    }


def test_delete_data_not_found():
    response = client.delete("/posts/Deneme")
    assert response.status_code == 404
    assert response.json() == {"message": "Post with title 'Deneme' not found"}
