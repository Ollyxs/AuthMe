import unittest
import redis

class TestRedisConnection(unittest.TestCase):

    def test_redis_connection(self):
        redis_client = redis.Redis(host='localhost', port=6380, password='qwerty')
        self.assertTrue(redis_client.ping())
