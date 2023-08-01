import httpx
import json

import pytest
import pytest_asyncio

BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.asyncio
async def test_read_all_empty():
    async with httpx.AsyncClient() as client:
        resp: client = await client.get(f"{BASE_URL}/books")
        assert resp.status_code == 200
        assert resp.text == "[]"


@pytest.mark.asyncio
async def test_create_book():
    new_book_data = {
        "title": "The lord of the rings",
        "year": "1950", "authors": []
    }
    new_book_data_json = json.dumps(new_book_data)
    async with httpx.AsyncClient() as client:
        resp: client = await client.post(f"{BASE_URL}/books", data=new_book_data_json)  # noqa 501
        assert resp.status_code == 201


@pytest.mark.asyncio
async def test_create_author():
    new_author_data = {
        "name": "J.R.R Tolkien",
        "country": "England", "books": []
    }
    new_author_data_json = json.dumps(new_author_data)
    async with httpx.AsyncClient() as client:
        resp: client = await client.post(f"{BASE_URL}/authors", data=new_author_data_json)  # noqa 501
        assert resp.status_code == 201


@pytest.mark.asyncio
async def test_create_relation():
    async with httpx.AsyncClient() as client:
        resp: client = await client.post(f"{BASE_URL}/books/1/authors/1/")
        assert resp.text == '{"message":"Author added to book successfully"}'


@pytest.mark.asyncio
async def test_relation():
    async with httpx.AsyncClient() as client:
        resp: client = await client.get(f"{BASE_URL}/books/1")
        pyth_resp = json.loads(resp.text)
        authors = pyth_resp.get("authors")
        assert authors[0] == {"id": 1,
                              "name": "J.R.R Tolkien",
                              "country": "England"
                              }


@pytest.mark.asyncio
async def test_deletion():
    async with httpx.AsyncClient() as client:
        resp: client = await client.delete(f"{BASE_URL}/cleardb")
        assert resp.status_code == 204

