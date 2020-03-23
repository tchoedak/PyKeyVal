from sqlalchemy.engine.url import make_url
from sqlalchemy import create_engine


class PyKeyVal(object):

	def __init__(self, url, name, namespace=None, **options):
		self.url = url
		self.name = name
		self.namespace = namespace
		self.options = options
		self.stores = {
			'snowflake': SnowKeyVal
		}
		self._store = self.stores.get(options.get('store')) or self._store_from_url(url) # loads the underlying store Object
		self.engine = create_engine(url)

		if self._store:
			self.store = store(engine=self.engine, name=self.name, namespace=self.namespace**options)
		else:
			raise ValueError('Unable to find an adequate store. Please use one of', self.stores)

	def _store_from_url(self, url):
		backend = make_url(url).get_backend_name()
		return backend

	def set(self, key, value, ttl=None):
		self.store.set(key, value)

	def get(self, key):
		self.store.set(key)

	def delete(self, key):
		self.store.delete(key)

	def clear(self):
		self.store.clear()

