import httpx
import json


BASE_URL = "http://localhost:8000"


def test_read_all_empty():
    resp: httpx = httpx.get(f"{BASE_URL}/books")
    assert resp.status_code == 200
    assert resp.text == "[]"


def test_create_book():
    new_book_data = {
        "title": "The lord of the rings",
        "year": "1950", "authors": []
    }
    new_book_data_json = json.dumps(new_book_data)
    resp: httpx = httpx.post(f"{BASE_URL}/books", data=new_book_data_json)  # noqa 501
    assert resp.status_code == 201


def test_create_author():
    new_author_data = {
        "name": "J.R.R Tolkien",
        "country": "England", "books": []
    }
    new_author_data_json = json.dumps(new_author_data)
    resp: httpx = httpx.post(f"{BASE_URL}/authors", data=new_author_data_json)  # noqa 501
    assert resp.status_code == 201


def test_create_relation():
    resp: httpx = httpx.post(f"{BASE_URL}/books/1/authors/1/")
    assert resp.text == '{"message":"Author added to book successfully"}'


def test_relation():
    resp: httpx = httpx.get(f"{BASE_URL}/books/1")
    pyth_resp = json.loads(resp.text)
    authors = pyth_resp.get("authors")
    assert authors[0] == {"id": 1,
                          "name": "J.R.R Tolkien",
                          "country": "England"
                          }


def test_deletion():
    resp: httpx = httpx.delete(f"{BASE_URL}/cleardb")
    assert resp.status_code == 204
