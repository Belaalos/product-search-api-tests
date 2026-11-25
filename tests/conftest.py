import pytest
import requests

BASE_URL = "https://api.practicesoftwaretesting.com"


@pytest.fixture(scope="session")
def get():
    session = requests.Session()

    def _get(path, **params):
        return session.get(BASE_URL + path, params=params, timeout=20)

    return _get


@pytest.fixture(scope="session")
def first_page(get):
    resp = get("/products")
    assert resp.status_code == 200
    return resp.json()
