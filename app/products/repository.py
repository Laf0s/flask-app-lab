import os
import uuid
from datetime import datetime
from tinydb import TinyDB, Query
from flask import current_app

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
DB_PATH = os.path.join(DATA_DIR, "products.json")


def get_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    return TinyDB(DB_PATH)


def get_next_id():
    db = get_db()
    products = db.all()
    if not products:
        return 1
    return max(p.get("id", 0) for p in products) + 1


def get_all_products():
    db = get_db()
    return db.all()


def get_product_by_id(product_id: int):
    db = get_db()
    Product = Query()
    return db.get(Product.id == product_id)


def save_uploaded_image(image_file):
    if not image_file or not hasattr(image_file, "filename") or not image_file.filename:
        return None

    upload_folder = os.path.join(current_app.root_path, "static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    ext = os.path.splitext(image_file.filename)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{ext}"

    file_path = os.path.join(upload_folder, unique_filename)
    image_file.save(file_path)
    return f"uploads/{unique_filename}"


def create_product(data, image_file=None):
    db = get_db()
    new_id = get_next_id()
    image_rel_path = save_uploaded_image(image_file)

    record = {
        "id": new_id,
        "name": data["name"],
        "content": data["content"],
        "price": float(data["price"]),
        "category": data["category"],
        "quantity": int(data["quantity"]),
        "image": image_rel_path,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db.insert(record)
    return new_id


def update_product(product_id: int, data, image_file=None):
    db = get_db()
    Product = Query()
    existing = db.get(Product.id == product_id)
    if not existing:
        return False

    image_rel_path = existing.get("image")

    if image_file and hasattr(image_file, "filename") and image_file.filename:
        new_image = save_uploaded_image(image_file)
        if new_image:
            image_rel_path = new_image

    db.update({
        "name": data["name"],
        "content": data["content"],
        "price": float(data["price"]),
        "category": data["category"],
        "quantity": int(data["quantity"]),
        "image": image_rel_path
    }, Product.id == product_id)
    return True


def delete_product(product_id: int):
    db = get_db()
    Product = Query()
    removed = db.remove(Product.id == product_id)
    return len(removed) > 0