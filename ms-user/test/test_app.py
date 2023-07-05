# import unittest
# from flask import Flask
# from main import create_app


# class AppTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app()
#         self.app_context = self.app.app_context()
#         self.app_context.push()

#     def tearDown(self):
#         self.app_context.pop()

#     def test_app_creation(self):
#         self.assertIsInstance(self.app, Flask)