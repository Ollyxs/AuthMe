import unittest
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required
from flask_sqlalchemy import SQLAlchemy
from main import db
from main.models import UserModel
from main.controllers import UserResource, UsersResource


class UserCrudTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://authme:qwerty@172.19.0.5/authme'
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.init_app(self.app)
        db.create_all()

        jwt = JWTManager(self.app)

        self.api.add_resource(UserResource, '/user/<int:id>')
        self.api.add_resource(UsersResource, '/users')

        self.client = self.app.test_client()

        with self.app.app_context():
            user = UserModel(
                name='John',
                last_name='Wick',
                email="john.wick@exampĺe.com",
                plain_password='password123',
                role='user'
            )
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_database_creation(self):
        self.assertIsInstance(db, SQLAlchemy)

    @jwt_required
    def test_get_user(self):
        response = self.client.get('/user/1')
        self.assertEqual(response.status_code, 201)

    @jwt_required
    def test_put_user(self):
        user_data = {
            'name': 'Mike',
            'last_name': 'Wick',
            'email': 'mike.wick@example.com',
            'password': 'newpassword',
            'role': 'admin'
        }
        response = self.client.put(f'/user/1', json=user_data)
        self.assertEqual(response.status_code, 201)

    @jwt_required
    def test_delete_user(self):
        response = self.client.delete('/user/1')
        self.assertEqual(response.status_code, 204)

    @jwt_required
    def test_get_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

    @jwt_required
    def test_post_user(self):
        user_data = {
            'name': 'Jane',
            'last_name': 'Wick',
            'email': 'jane.wick@example.com',
            'password': 'password123',
            'role': 'user'
        }
        response = self.client.post('/users', json=user_data)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()