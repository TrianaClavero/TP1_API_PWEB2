from flask import Flask, request
import json
from pathlib import Path
app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
PRODUCTS_FILE = BASE_DIR / "products.json"
STORE = {"products": [], "cart": []}


def initialize_store():
    try:
        with PRODUCTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    STORE["products"] = data.get("products", [])
    STORE["cart"] = []


def load_products():
    return STORE["products"]

@app.route('/')
def alive():
    return "I'm alive!"

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return product
    return {"error": "Product not found"}, 404

@app.route('/products', methods=['GET'])
def get_all_products():
    return {"products": load_products()}

@app.route('/cart', methods=['GET'])
def get_cart():
    return {"cart": STORE["cart"]}

@app.route('/cart/items', methods=['POST'])
def add_to_cart():
    payload = request.get_json(silent=True) or {}
    product_id = payload.get("product_id")

    if not isinstance(product_id, int):
        return {"error": "product_id must be an integer"}, 400
    products = STORE["products"]
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return {"error": "Product not found"}, 404
    cart = STORE["cart"]
    cart_item = next((item for item in cart if item["product_id"] == product_id), None)
    if cart_item:
        try:
            cart_item["quantity"] = int(cart_item.get("quantity", 0))
        except (TypeError, ValueError):
            return {"error": "Invalid quantity in cart data"}, 400
        cart_item["quantity"] += 1
    else:
        cart.append({"product_id": product_id, "quantity": 1})
    return {"message": "Product added to cart."}, 200

@app.route('/cart/items/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    cart = STORE["cart"]
    cart_item = next((item for item in cart if item["product_id"] == product_id), None)
    if not cart_item:
        return {"error": "Product not in cart"}, 404
    try:
        quantity = int(cart_item.get("quantity", 0))
    except (TypeError, ValueError):
        return {"error": "Invalid quantity in cart data"}, 400
    if quantity <= 0:
        return {"error": "Product not in cart"}, 404
    cart_item["quantity"] = quantity - 1
    if cart_item["quantity"] == 0:
        STORE["cart"] = [item for item in cart if item["product_id"] != product_id]
    return {"message": "Product removed from cart."}, 200

@app.route('/cart/total', methods=['GET'])
def calculate_total():
    cart = STORE["cart"]
    products = STORE["products"]
    total = 0
    for item in cart:
        product = next((p for p in products if p["id"] == item["product_id"]), None)
        if product:
            total += product["price"] * item["quantity"]
    return {"total": total}

initialize_store()

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)

