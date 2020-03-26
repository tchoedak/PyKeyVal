from sqlalchemy.engine.url import make_url
from . import serializers


class PyKeyVal(object):
    def __init__(self, url, name, namespace=None, serializer=None, **options):
        self.url = url
        self.name = name
        self.namespace = namespace
        self.options = options
        self.serializer = serializer or JsonSerializer
        self.stores = {'snowflake': SnowKeyVal, 'dict': DictKeyVal}
        self._store = self.stores.get(options.get('store')) or self.stores.get(
            self._store_from_url(url)
        )  # loads the underlying store Object

        if self._store:
            self.store = self._store(
                url=self.url, name=self.name, namespace=self.namespace, **options
            )
        else:
            raise ValueError(
                'Unable to find an adequate store. Please use one of', self.stores
            )

    def _store_from_url(self, url):
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
        return self._deserialize(self.store.get(key))

    def delete(self, key):
        return self.store.delete(key)

    def clear(self):
        return self.store.clear()
