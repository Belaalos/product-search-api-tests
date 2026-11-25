def test_sort_by_price_descending(get):
    prices = [p["price"] for p in get("/products", sort="price,desc").json()["data"]]
    assert prices == sorted(prices, reverse=True)


def test_sort_by_price_ascending(get):
    prices = [p["price"] for p in get("/products", sort="price,asc").json()["data"]]
    assert prices == sorted(prices)


def test_sort_by_name_ascending(get):
    names = [p["name"] for p in get("/products", sort="name,asc").json()["data"]]
    assert names == sorted(names)


def test_price_range_filter(get):
    resp = get("/products", between="price,1,10")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data
    assert all(1 <= p["price"] <= 10 for p in data)


def test_filter_by_brand(get):
    brand = get("/brands").json()[0]
    data = get("/products", by_brand=brand["id"]).json()["data"]
    assert data
    assert all(p["brand"]["id"] == brand["id"] for p in data)


def test_filter_by_category(get):
    category = get("/categories").json()[0]["id"]
    resp = get("/products", by_category=category)
    assert resp.status_code == 200
    assert resp.json()["total"] >= 0


def test_eco_friendly_filter(get):
    data = get("/products", eco_friendly="true").json()["data"]
    assert data
    assert all(p["is_eco_friendly"] for p in data)


def test_search_finds_hammers(get):
    resp = get("/products/search", q="hammer")
    assert resp.status_code == 200
    names = [p["name"].lower() for p in resp.json()["data"]]
    assert names and all("hammer" in n for n in names)


def test_search_without_results(get):
    resp = get("/products/search", q="zzzzzz")
    assert resp.status_code == 200
    assert resp.json()["total"] == 0
