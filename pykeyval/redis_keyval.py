import redis

'''
Implements a KeyVal Store with Redis as the backend
'''


class RedisKeyVal(object):
    '''
    Implements a PyKeyVal interface to redis.

    An instance can be connected to redis from URLs following these patterns
        redis://[[username]:[password]]@localhost:6379/0
        rediss://[[username]:[password]]@localhost:6379/0
        unix://[[username]:[password]]@/path/to/socket.sock?db=0
    '''

    def __init__(self, url, **options):
        self.url = url
        self.redis = redis.Redis.from_url(url)
        self.options = options

    def get(self, key):
        val = self.redis.get(key)
        if val:
            val = val.decode('utf-8')
        return val

    def set(self, key, val):
        return self.redis.set(key, val)

    def delete(self, key):
        return self.redis.delete(key) == 1

    def clear(self):
        return self.redis.flushdb()
