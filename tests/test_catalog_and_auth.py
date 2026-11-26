import requests

from conftest import BASE_URL


def test_brands_list(get):
    brands = get("/brands").json()
    assert len(brands) >= 2
    assert all({"id", "name", "slug"} <= set(b) for b in brands)


def test_categories_list_has_parent_links(get):
    categories = get("/categories").json()
    assert categories
    parents = {c["id"] for c in categories}
    children = [c for c in categories if c.get("parent_id")]
    assert children
    assert all(c["parent_id"] in parents for c in children)


def test_category_tree_is_available(get):
    resp = get("/categories/tree")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def post_login(body):
    """The public server sometimes answers 500 for a moment (seen once in CI), so retry once."""
    resp = requests.post(f"{BASE_URL}/users/login", json=body, timeout=20)
    if resp.status_code >= 500:
        resp = requests.post(f"{BASE_URL}/users/login", json=body, timeout=20)
    return resp


def test_login_with_wrong_credentials_is_unauthorized():
    resp = post_login({"email": "nobody@example.com", "password": "wrong"})
    assert resp.status_code == 401
    assert resp.json() == {"error": "Unauthorized"}


def test_login_with_empty_body_is_unauthorized():
    resp = post_login({})
    assert resp.status_code == 401


def test_profile_without_token_is_unauthorized(get):
    assert get("/users/me").status_code == 401
