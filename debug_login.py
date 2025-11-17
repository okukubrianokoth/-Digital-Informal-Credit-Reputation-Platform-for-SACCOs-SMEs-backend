from app import create_app, db
from app.models.user import User

app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

with app.app_context():
    db.create_all()
    user = User(full_name='Test User', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

client = app.test_client()
resp = client.post('/api/auth/login', json={'email':'test@example.com','password':'password123'})
print('status:', resp.status_code)
try:
    print('json:', resp.get_json())
except Exception as e:
    print('get_json error:', e)
print('data bytes:', resp.data)
