# flake8: noqa
import unittest
import os
from datetime import datetime
from flask_mail import Message, Mail
from flask import abort
import tests.init_dotenv  # initialize env vars here
from lsfd202201.models import db, Article, Comment
from lsfd202201 import create_app


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.mail = Mail(self.app)
        self.context = self.app.app_context()
        self.context.push()
        self.client = self.app.test_client()
        self.dt = datetime.now()
        db.drop_all()
        db.create_all()

    def tearDown(self) -> None:
        db.drop_all()
        db.session.remove()
        self.context.pop()

    def login_as_admin(self):
        data = {
            'admin_name': os.getenv("ADMIN_TWO_NAME"),
            'password': os.getenv("ADMIN_PASSWORD")
        }
        response = self.client.post("/admin/", data=data)
        return response

    def create_article(self, body):
        dt = self.dt
        data = {
            'name': 'test_bot',
            'password': os.getenv("ADMIN_PASSWORD"),
            'date': f"{dt.year}-{dt.month}-{dt.day}",
            'title': 'unittest',
            'content': body
        }
        response = self.client.post("/articles/upload-result/", data=data)
        return response

    def create_comment(self, body):
        data = {
            'name': 'test_bot',
            'body': body
        }
        response = self.client.post("/comments/", data=data)
        return response

    def test_app_exists(self):
        self.assertIsNotNone(self.app)

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])

    def test_200(self):
        self.assertTrue(
            self.client.get('/').status_code == 200 and
            self.client.get('/index/').status_code == 200 and
            self.client.get('/articles/').status_code == 200 and
            self.client.get('/articles/upload/').status_code == 200 and
            self.client.get('/main/').status_code == 200 and
            self.client.get('/members/').status_code == 200 and
            self.client.get('/articles/').status_code == 200 and
            self.client.get('/video/').status_code == 200 and
            self.client.get('/kzkt/').status_code == 200 and
            self.client.get('/about/').status_code == 200 and
            self.client.get('/about-zh/').status_code == 200 and
            self.client.get('/comments/').status_code == 200
        )

    def test_302(self):
        self.assertEqual(self.client.get('/admin/').status_code, 302)

    def test_404(self):
        self.assertEqual(self.client.get("/thisDoesn'tExist").status_code, 404)

    def test_405(self):
        self.assertEqual(
            self.client.get('/articles/upload-result/').status_code, 405
        )
        self.assertEqual(
            self.client.get('/admin/articles/edit_result/1').status_code, 405
        )

    def test_500(self):
        @self.app.route('/500')
        def internal_server_error_for_testing():
            abort(500)

        response = self.client.get('/500')
        received_data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 500)
        self.assertIn("500 Internal Server Error", received_data)
        self.assertIn("nav", received_data)

    def test_400(self):
        @self.app.route('/400')
        def internal_server_error_for_testing():
            abort(400)

        response = self.client.get('/400')
        received_data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn("400 Bad Request", received_data)
        self.assertIn("nav", received_data)

    def test_add_article(self):
        article = Article(
            title="Test",
            author="Test",
            date="Test",
            content="Test"
        )
        self.assertEqual(str(article), "<Article Test>")
        db.session.add(article)
        db.session.commit()
        self.assertIsNotNone(Article().query_by_id(1))
        self.assertEqual(self.client.get('/articles/').status_code, 200)
        Article().delete_by_id(1)
        self.assertIsNone(Article().query_by_id(1))

    def test_upload(self):
        dt = self.dt
        data = {
            'name': 'test_bot',
            'password': "WrongPassword",
            'date': f"{dt.year}-{dt.month}-{dt.day}",
            'title': 'unittest',
            'content': 'TESTING'
        }
        response = self.client.post("/articles/upload-result/", data=data)
        received_data = response.get_data(as_text=True)
        self.assertIn("Wrong Password", received_data)
        self.assertEqual(len(Article().query_all()), 0)
        response = self.create_article('TESTING')
        received_data = response.get_data(as_text=True)
        self.assertIn("Upload Success", received_data)
        self.assertNotEqual(len(Article().query_all()), 0)

    def test_comments(self):
        data = {
            'name': 'test_bot',
            'body': 'Unittest'
        }
        response = self.client.post("/comments/", data=data)
        self.assertEqual(response.status_code, 200)
        received_data = response.get_data(as_text=True)
        self.assertIn("Unittest", received_data)

    def test_emails(self):
        with self.mail.record_messages() as outbox:
            msg = Message(
                recipients=self.app.config["ADMIN_EMAIL_LIST"],
                subject="LSFD202201 Project Unittest",
                body="Plain Text",
                html="<strong>HTML</strong> <em>Content</em>"
            )
            self.mail.send(msg)
            self.assertGreater(len(outbox), 0)
            self.assertEqual(outbox[0].subject, "LSFD202201 Project Unittest")

    def test_admin_basic(self):
        response = self.client.get("/admin/logout/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/admin/comments/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 200)
        self.login_as_admin()
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/admin/comments/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/admin/logout/")
        self.assertEqual(response.status_code, 302)

    def test_admin_login(self):
        data = {
            'admin_name': os.getenv("ADMIN_TWO_NAME"),
            'password': 'WrongPassword'
        }
        response = self.client.post("/admin/articles/", data=data)
        self.assertEqual(response.status_code, 302)
        data['password'] = os.getenv("ADMIN_PASSWORD")
        response = self.client.post("/admin/articles/", data=data)
        self.assertEqual(response.status_code, 200)
        received_data = response.get_data(as_text=True)
        self.assertIn("Welcome, Administrator", received_data)

    def test_admin_delete(self):
        self.login_as_admin()
        self.create_article("Hello, World!")
        response = self.client.post("/admin/articles/delete/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Article().query_all()), 0)

    def test_admin_edit_post(self):
        self.login_as_admin()
        self.create_article("Goodbye, World!")
        data = {
            'ckeditor': "Hello, World!"
        }
        response = self.client.post("/admin/articles/edit_result/1", data=data)
        self.assertEqual(response.status_code, 200)
        received_data = response.get_data(as_text=True)
        self.assertIn("Edit Succeeded!", received_data)
        article = Article().query_by_id(1)
        self.assertEqual(article.content, "Hello, World!")

    def test_admin_delete_comment(self):
        self.login_as_admin()
        self.create_comment("Hello, World!")
        self.assertGreater(len(Comment().query_all()), 0)
        response = self.client.post("/admin/comments/delete/1")
        self.assertEqual(response.status_code, 200)
        received_data = response.get_data(as_text=True)
        self.assertIn("deleted", received_data)
