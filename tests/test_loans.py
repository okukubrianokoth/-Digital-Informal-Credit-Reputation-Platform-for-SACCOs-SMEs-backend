import unittest
from app import create_app, db
from app.models.user import User
from app.models.loan import Loan

class LoanTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        with self.app.app_context():
            db.create_all()
            user = User(full_name="Loan User", email="loan@example.com")
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_apply_loan(self):
        response = self.client.post("/api/loans/", json={
            "user_id": self.user_id,
            "amount": 1000,
            "term_months": 6
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["amount"], 1000)
        self.assertEqual(data["status"], "pending")

if __name__ == "__main__":
    unittest.main()
