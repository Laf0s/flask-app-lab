import os
import unittest
import warnings
from unittest.mock import patch
from app import app
from app.products.repository import get_db, create_product

TEST_DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "test_products.json")
)


class ProductBlueprintTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=ResourceWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        cls.patcher = patch("app.products.repository.DB_PATH", TEST_DB_PATH)
        cls.patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except OSError:
                pass

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

        db = get_db()
        db.truncate()
        db.close()

        self.test_product_id = create_product({
            "name": "Ноутбук Lenovo IdeaPad",
            "content": "Швидкий ноутбук для навчання та роботи з 16 ГБ RAM.",
            "price": "650.00",
            "category": "computers",
            "quantity": "7"
        })

    def tearDown(self):
        db = get_db()
        db.truncate()
        db.close()

    def test_products_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ноутбук Lenovo IdeaPad".encode("utf-8"), response.data)
        self.assertIn(b"650.00", response.data)

    def test_product_detail_page(self):
        response = self.client.get(f"/products/{self.test_product_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ноутбук Lenovo IdeaPad".encode("utf-8"), response.data)
        self.assertIn("Швидкий ноутбук для навчання".encode("utf-8"), response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/99999")
        self.assertEqual(response.status_code, 404)

    def test_create_product_success(self):
        data = {
            "name": "Миша Бездротова",
            "content": "Оптична бездротова миша з підтримкою Bluetooth 5.0.",
            "price": "29.99",
            "category": "peripherals",
            "quantity": "15"
        }
        response = self.client.post("/products/add", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Миша Бездротова".encode("utf-8"), response.data)

    def test_create_product_validation_error(self):
        data = {
            "name": "AB",
            "content": "Опис",
            "price": "10.00",
            "category": "electronics",
            "quantity": "2"
        }
        response = self.client.post("/products/add", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Мінімум 3 символи".encode("utf-8"), response.data)

    def test_update_product_success(self):
        update_data = {
            "name": "Оновлений Ноутбук Pro",
            "content": "Оновлений опис товару після модернізації.",
            "price": "799.50",
            "category": "computers",
            "quantity": "4"
        }
        response = self.client.post(
            f"/products/{self.test_product_id}/edit",
            data=update_data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Оновлений Ноутбук Pro".encode("utf-8"), response.data)
        self.assertIn(b"799.50", response.data)

    def test_delete_product_success(self):
        response = self.client.post(
            f"/products/{self.test_product_id}/delete",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Ноутбук Lenovo IdeaPad".encode("utf-8"), response.data)


if __name__ == "__main__":
    unittest.main()