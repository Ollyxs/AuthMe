import unittest, sys
from sqlalchemy import text


sys.path.append('../')
from app import create_app, db

class ConnectionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testDbConection(self):
        result = db.session.query(text("'Hello, world'")).one()
        self.assertEqual(result[0], 'Hello, world')