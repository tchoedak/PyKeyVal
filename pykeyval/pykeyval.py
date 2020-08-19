from sqlalchemy.engine.url import make_url
from .serializers import JsonSerializer
from .snow_keyval import SnowKeyVal
from .dict_keyval import DictKeyVal
from .file_keyval import FileKeyVal
from .redis_keyval import RedisKeyVal
from .sqlite_keyval import SQLiteKeyVal



class PyKeyVal(object):
    def __init__(self, url='', name=None, **options):
        self.url = url
        self.name = name
        self.options = options
        self.serializer = options.get('serializer') or JsonSerializer
        self.stores = {
            'snowflake': SnowKeyVal,
            'dict': DictKeyVal,
            'file': FileKeyVal,
            'sqlite': SQLiteKeyVal,
            'redis': RedisKeyVal,
        }
        self.store = self._default_store(url, options)(url=url, name=name, **options)

    def _default_store(self, url, options):
        if options.get('store'):
            return self.stores.get(options.get('store'))
        if url:
            try:
                return self.stores.get(self._store_from_sql_url(url))
            except:
                # handle stores from non_sql urls such as redis/mongo.
                pass

    def _store_from_sql_url(self, url):
        backend = make_url(url).get_backend_name()
        return backend

    def _serialize(self, val):
        return self.serializer.serialize(dict(_value=val))

    def _deserialize(self, val):
        return self.serializer.deserialize(val).get('_value')

    def set(self, key, val):
        self.store.set(key, self._serialize(val))
        return True

    def get(self, key):
        val = self.store.get(key)
        if val:
            return self._deserialize(val)

    def delete(self, key):
        '''
        Returns True if the key existed, False if not.
        '''
        return self.store.delete(key)

    def clear(self):
        '''
        Delete all entries in the current namespace
        '''
        return self.store.clear()
