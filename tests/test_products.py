import pytest
from jsonschema import validate

PRODUCT_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "price", "category", "brand", "in_stock"],
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "price": {"type": "number", "minimum": 0},
        "in_stock": {"type": "boolean"},
        "category": {"type": "object", "required": ["id", "name"]},
        "brand": {"type": "object", "required": ["id", "name"]},
    },
}


@pytest.mark.smoke
def test_product_list_has_pagination_fields(first_page):
    for key in ("current_page", "data", "from", "last_page", "per_page", "to", "total"):
        assert key in first_page
    assert first_page["current_page"] == 1
    assert len(first_page["data"]) == first_page["per_page"]


def test_every_product_on_page_matches_schema(first_page):
    for product in first_page["data"]:
        validate(product, PRODUCT_SCHEMA)


def test_second_page_has_different_products(get, first_page):
    page2 = get("/products", page=2).json()
    assert page2["current_page"] == 2
    ids1 = {p["id"] for p in first_page["data"]}
    ids2 = {p["id"] for p in page2["data"]}
    assert ids1.isdisjoint(ids2)


def test_page_count_matches_total(first_page):
    expected_pages = -(-first_page["total"] // first_page["per_page"])
    assert first_page["last_page"] == expected_pages


def test_page_beyond_last_returns_empty_list(get):
    resp = get("/products", page=999)
    assert resp.status_code == 200
    assert resp.json()["data"] == []


def test_product_details_match_list_entry(get, first_page):
    listed = first_page["data"][0]
    detail = get(f"/products/{listed['id']}")
    assert detail.status_code == 200
    body = detail.json()
    assert body["id"] == listed["id"]
    assert body["name"] == listed["name"]
    assert body["price"] == listed["price"]


def test_unknown_product_returns_404(get):
    resp = get("/products/DOES_NOT_EXIST")
    assert resp.status_code == 404
    assert resp.json()["message"] == "Requested item not found"
