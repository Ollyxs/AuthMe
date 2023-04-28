import unittest
import redis

class TestRedisConnection(unittest.TestCase):

    def test_redis_connection(self):
        redis_client = redis.Redis(host='redis', port=6380)
        self.assertTrue(redis_client.ping())
