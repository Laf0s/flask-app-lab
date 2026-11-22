import unittest
from app import create_app, db
from app.users.models import User


class AuthTestsCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("test")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login_pages_load(self):
        res_reg = self.client.get("/users/register")
        self.assertEqual(res_reg.status_code, 200)
        self.assertIn("Register", res_reg.get_data(as_text=True))

        res_login = self.client.get("/users/login")
        self.assertEqual(res_login.status_code, 200)
        self.assertIn("Login", res_login.get_data(as_text=True))

    def test_user_registration_saves_hashed_password(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "testuser1",
                "email": "testuser1@example.com",
                "password": "secretpassword",
                "confirm_password": "secretpassword",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Account created for testuser1!", response.get_data(as_text=True))

        user = db.session.scalar(db.select(User).where(User.email == "testuser1@example.com"))
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser1")
        self.assertNotEqual(user.password, "secretpassword")
        self.assertTrue(user.check_password("secretpassword"))

    def test_duplicate_registration_fails(self):
        existing = User(username="oscar", email="oscar@example.com", password="")
        existing.set_password("password123")
        db.session.add(existing)
        db.session.commit()

        response = self.client.post(
            "/users/register",
            data={
                "username": "oscar",
                "email": "oscar@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("вже існує", response.get_data(as_text=True))

    def test_login_logout_and_protected_routes(self):
        res_unauth = self.client.get("/users/account")
        self.assertEqual(res_unauth.status_code, 302)
        self.assertIn("/users/login", res_unauth.headers["Location"])

        user = User(username="validuser", email="valid@example.com", password="")
        user.set_password("mypassword")
        db.session.add(user)
        db.session.commit()

        res_bad = self.client.post(
            "/users/login",
            data={"email": "valid@example.com", "password": "wrongpassword"},
            follow_redirects=True,
        )
        self.assertIn("Невірний email або пароль", res_bad.get_data(as_text=True))

        res_login = self.client.post(
            "/users/login",
            data={"email": "valid@example.com", "password": "mypassword", "remember": False},
            follow_redirects=True,
        )
        html_account = res_login.get_data(as_text=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn("Welcome, validuser!", html_account)
        self.assertIn("valid@example.com", html_account)

        res_list = self.client.get("/users/list")
        self.assertEqual(res_list.status_code, 200)
        self.assertIn("Users List (1)", res_list.get_data(as_text=True))

        res_logout = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(res_logout.status_code, 200)
        self.assertIn("You have successfully logged out.", res_logout.get_data(as_text=True))

        res_after_logout = self.client.get("/users/account")
        self.assertEqual(res_after_logout.status_code, 302)


if __name__ == "__main__":
    unittest.main()