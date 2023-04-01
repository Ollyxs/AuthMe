import unittest, sys
sys.path.append('../')
from app import create_app, db
from main.models import UserModel


class UserCrudTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        user_data = {
            'name': 'john',
            'last_name' : 'wick',
            'email': 'john@example.com',
            'password': 'testpass',
            'role': 'admin'
        }
        response = self.client.post('/users', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['name'], user_data['name'])
        self.assertEqual(response.json['last_name'], user_data['last_name'])
        self.assertEqual(response.json['email'], user_data['email'])
        self.assertFalse('password' in response.json)
        self.assertFalse('role' in response.json)

    def test_get_user(self):
        user = UserModel(name='jane', email='jane@example.com', password='testpass', last_name="asd", role="admin")
        db.session.add(user)
        db.session.commit()
        response = self.client.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], user.name)
        self.assertEqual(response.json['last_name'], user.last_name)
        self.assertEqual(response.json['email'], user.email)
        self.assertFalse('password' in response.json)
        self.assertFalse('role' in response.json)
    
    
    def test_update_user(self):
        user = UserModel(name='jane', email='jane@example.com', password='testpass', role='admin', last_name="asd")
        db.session.add(user)
        db.session.commit()
        user_data = {
            'name': 'jane_updated',
            'email': 'jane_updated@example.com'
        }
        response = self.client.put(f'/users/{user.id}', json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], user_data['name'])
        self.assertEqual(response.json['email'], user_data['email'])
        self.assertEqual(response.json['last_name'], user_data['last_name'])
        self.assertFalse('password' in response.json)
        updated_user = UserModel.query.get(user.id)
        self.assertEqual(updated_user.name, user_data['name'])
        self.assertEqual(updated_user.last_name, user_data['last_name'])
        self.assertEqual(updated_user.email, user_data['email'])

    def test_delete_user(self):
        user = UserModel(name='jane', email='jane@example.com', password='testpass', last_name='asd', role='admin')
        db.session.add(user)
        db.session.commit()
        response = self.client.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(UserModel.query.get(user.id))