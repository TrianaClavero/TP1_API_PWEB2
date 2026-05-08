import pytest

import app as app_module


@pytest.fixture(autouse=True)
def reset_store():
    app_module.STORE["products"] = [
        {"id": 1, "name": "Product A", "price": 10.0, "description": "A"},
        {"id": 2, "name": "Product B", "price": 20.0, "description": "B"},
    ]
    app_module.STORE["cart"] = []


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as test_client:
        yield test_client


def test_get_products_returns_available_products(client):
    response = client.get("/products")

    assert response.status_code == 200
    body = response.get_json()
    assert "products" in body
    assert len(body["products"]) == 2


def test_get_single_product_found(client):
    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_single_product_not_found(client):
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"


def test_add_to_cart_adds_new_item(client):
    response = client.post("/cart/items", json={"product_id": 1})

    assert response.status_code == 200
    assert app_module.STORE["cart"] == [{"product_id": 1, "quantity": 1}]


def test_add_to_cart_increments_existing_item(client):
    app_module.STORE["cart"] = [{"product_id": 1, "quantity": 1}]

    response = client.post("/cart/items", json={"product_id": 1})

    assert response.status_code == 200
    assert app_module.STORE["cart"][0]["quantity"] == 2


def test_add_to_cart_requires_integer_product_id(client):
    response = client.post("/cart/items", json={"product_id": "1"})

    assert response.status_code == 400
    assert response.get_json()["error"] == "product_id must be an integer"


def test_add_to_cart_product_not_found(client):
    response = client.post("/cart/items", json={"product_id": 999})

    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"


def test_remove_from_cart_decrements_quantity(client):
    app_module.STORE["cart"] = [{"product_id": 1, "quantity": 2}]

    response = client.delete("/cart/items/1")

    assert response.status_code == 200
    assert app_module.STORE["cart"][0]["quantity"] == 1


def test_remove_from_cart_removes_item_when_quantity_reaches_zero(client):
    app_module.STORE["cart"] = [{"product_id": 1, "quantity": 1}]

    response = client.delete("/cart/items/1")

    assert response.status_code == 200
    assert app_module.STORE["cart"] == []


def test_remove_from_cart_returns_404_when_item_is_not_present(client):
    response = client.delete("/cart/items/1")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not in cart"


def test_calculate_total_sums_cart_items(client):
    app_module.STORE["cart"] = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1},
    ]

    response = client.get("/cart/total")

    assert response.status_code == 200
    assert response.get_json()["total"] == pytest.approx(40.0)
