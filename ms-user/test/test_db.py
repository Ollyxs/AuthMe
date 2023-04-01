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
<<<<<<< HEAD
        self.assertEqual(result[0], 'Hello, world')
=======
        self.assertEqual(result[0], 'Hello, world')
>>>>>>> 1232750d32f66dfcf180c3f8214c18316fdb13b7
