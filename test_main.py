from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_blogs():
    respose = client.get("/blog/all?page=1")
    assert respose.status_code == 200

def test_auth_error():
    respose = client.post("/token",
                          data={"username": "", "password": ""}
                          )
    access_token = respose.json().get("access_token")
    assert access_token == None
    message = respose.json().get("detail")[0].get("msg")
    assert message == "Field required"

def test_auth_success():
    respose = client.post("/token",
                          data={"username": "cat", "password": "cat"}
                          )
    access_token = respose.json().get("access_token")
    assert access_token 

def test_post_article():
    auth = client.post("/token",
                          data={"username": "cat", "password": "cat"}
                          )
    access_token = auth.json().get("access_token")
    assert access_token

    respose = client.post(
        "/article/",
        json={
             "title": "title1",
            "content": "content1",
            "published": True,
            "creator_id": 1
        },
        headers={
            "Authorization": "bearer " + access_token
        }
    )
    assert respose.status_code == 200
    assert respose.json().get("title") == "title1"