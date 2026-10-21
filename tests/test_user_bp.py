import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret-key"
        self.client = app.test_client()

    def test_greetings_page(self):
        response = self.client.get("/users/hi/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)

    def test_login_failed_with_wrong_credentials(self):
        response = self.client.post("/users/login", data={
            "username": "user1",
            "password": "wrong_password"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wrong data! Try again!", response.data)

    def test_profile_access_denied_without_session(self):
        response = self.client.get("/users/profile")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.headers["Location"])

    def test_successful_login_and_logout(self):
        login_res = self.client.post("/users/login", data={
            "username": "user1",
            "password": "password123"
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn("user1!".encode("utf-8"), login_res.data)

        profile_res = self.client.get("/users/profile")
        self.assertEqual(profile_res.status_code, 200)
        self.assertIn("Ласкаво просимо до сторінки".encode("utf-8"), profile_res.data)

        logout_res = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(logout_res.status_code, 200)
        self.assertIn("Ви вийшли із системи.".encode("utf-8"), logout_res.data)

    def test_cookie_add_and_delete(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"

        add_res = self.client.post("/users/cookie/add", data={
            "key": "test_city",
            "val": "Ivano-Frankivsk",
            "max_age": "3600"
        }, follow_redirects=True)
        self.assertEqual(add_res.status_code, 200)
        self.assertIn(b"test_city", add_res.data)

        del_res = self.client.post("/users/cookie/delete-by-key", data={
            "key_to_delete": "test_city"
        }, follow_redirects=True)
        self.assertEqual(del_res.status_code, 200)

    def test_theme_switcher(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"

        resp = self.client.get("/users/theme/dark", follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"bg-dark", resp.data)


if __name__ == "__main__":
    unittest.main()