# flake8: noqa
import unittest
import tests.init_dotenv
from lsfd202201.models import db, Article
from lsfd202201 import create_app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db.drop_all()
        db.session.remove()
        self.context.pop()

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
            self.client.get('/articles/').status_code == 200 and
            self.client.get('/video/').status_code == 200 and
            self.client.get('/kzkt/').status_code == 200 and
            self.client.get('/about/').status_code == 200 and
            self.client.get('/about-zh/').status_code == 200
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
            self.client.get('/admin/edit_result/1').status_code, 405
        )

    def test_upload(self):
        article = Article(
            title="Test",
            author="Test",
            date="Test",
            content="Test"
        )
        db.session.add(article)
        db.session.commit()
        self.assertIsNotNone(Article().query_by_id(1))
        Article().delete_by_id(1)
        self.assertIsNone(Article().query_by_id(1))
