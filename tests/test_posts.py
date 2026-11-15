import unittest
from datetime import datetime, timezone
from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "andrii"

        response = self.client.post("/posts/create", data={
            "title": "My first post",
            "content": "This is TDD in Flask!",
            "is_active": "y",
            "publish_date": "2026-11-15T14:00",
            "category": "tech"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Пост успішно створено".encode("utf-8"), response.data)

        with self.app.app_context():
            post = db.session.scalar(db.select(Post).where(Post.title == "My first post"))
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD in Flask!")
            self.assertEqual(post.author, "andrii")
            self.assertEqual(post.category, "tech")
            self.assertTrue(post.is_active)

    def test_create_post_anonymous_and_validation(self):
        bad_resp = self.client.post("/posts/create", data={
            "title": "A",
            "content": "Text",
            "category": "news"
        })
        self.assertEqual(bad_resp.status_code, 200)
        with self.app.app_context():
            self.assertEqual(db.session.scalar(db.select(db.func.count(Post.id))), 0)

        good_resp = self.client.post("/posts/create", data={
            "title": "Anonymous Post",
            "content": "Content from guest",
            "is_active": "y",
            "publish_date": "2026-11-15T14:30",
            "category": "news"
        }, follow_redirects=True)
        self.assertEqual(good_resp.status_code, 200)
        with self.app.app_context():
            post = db.session.scalar(db.select(Post).where(Post.title == "Anonymous Post"))
            self.assertEqual(post.author, "Anonymous")

    def test_list_posts(self):
        with self.app.app_context():
            p_old = Post(
                title="Older Post",
                content="Old text",
                posted=datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
                category="news",
                is_active=True
            )
            p_new = Post(
                title="Newer Post",
                content="New text",
                posted=datetime(2026, 11, 15, 10, 0, tzinfo=timezone.utc),
                category="tech",
                is_active=True
            )
            p_hidden = Post(
                title="Hidden Post",
                content="Secret",
                category="other",
                is_active=False
            )
            db.session.add_all([p_old, p_new, p_hidden])
            db.session.commit()

        response = self.client.get("/posts")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Newer Post", html)
        self.assertIn("Older Post", html)
        self.assertNotIn("Hidden Post", html)
        self.assertLess(html.index("Newer Post"), html.index("Older Post"))

    def test_view_post_detail(self):
        with self.app.app_context():
            post = Post(title="Detail Title", content="Full detailed content", category="publication", author="student")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.get(f"/posts/{post_id}")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Detail Title", html)
        self.assertIn("Full detailed content", html)
        self.assertIn("student", html)

    def test_update_post(self):
        with self.app.app_context():
            post = Post(title="Initial Title", content="Initial content", category="other", is_active=True)
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.post(f"/posts/{post_id}/update", data={
            "title": "Updated Title",
            "content": "Updated content",
            "is_active": "y",
            "publish_date": "2026-11-15T15:00",
            "category": "tech"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Пост оновлено".encode("utf-8"), response.data)

        with self.app.app_context():
            updated = db.session.get(Post, post_id)
            self.assertEqual(updated.title, "Updated Title")
            self.assertEqual(updated.content, "Updated content")
            self.assertEqual(updated.category, "tech")

    def test_delete_post(self):
        with self.app.app_context():
            post = Post(title="Post to Delete", content="Will be removed", category="news")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        get_resp = self.client.get(f"/posts/{post_id}/delete")
        self.assertEqual(get_resp.status_code, 200)
        self.assertIn("Post to Delete".encode("utf-8"), get_resp.data)

        post_resp = self.client.post(f"/posts/{post_id}/delete", follow_redirects=True)
        self.assertEqual(post_resp.status_code, 200)
        self.assertIn("Пост видалено".encode("utf-8"), post_resp.data)

        with self.app.app_context():
            self.assertIsNone(db.session.get(Post, post_id))

    def test_404_not_found(self):
        response = self.client.get("/posts/99999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()