import unittest
from app import create_app, db
from app.models.user import User
import json

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        
        with self.app.app_context():
            db.create_all()
            # Create a test user
            user = User(full_name="Test User", email="test@example.com")
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_login_success(self):
        response = self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", data)

    def test_login_fail_wrong_password(self):
        response = self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
