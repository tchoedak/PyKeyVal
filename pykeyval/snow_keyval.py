from types import new_class
from sqlalchemy import Table, MetaData, String, Column
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base
from snowflake.sqlalchemy import VARIANT
from sqlalchemy import func


def generate_keyval_model(table, tablename):

	class KeyVal(object):
		def __init__(self, key, val):
			__tablename__ = tablename
			self.key = key
			self.val = val

	mapper(KeyVal, table)
	return KeyVal


class SnowKeyVal(object):

	def __init__(self, engine, name, namespace=None, **options):
		self.engine = engine
		self._connection = None
		self._session = None
		self.meta = MetaData(self.engine)
		self.name = name
		self.namespace = namespace
		self.tablename = self.get_tablename(name, namespace)
		self.table = Table(
			self.tablename,
			self.meta,
			Column('key', String, primary_key=True),
			Column('val', VARIANT)
		)
		#self.create_table(self.tablename)
		self.table.create(checkfirst=True)
		self.KeyVal = generate_keyval_model(self.table, self.tablename)
		self.local_cache = {}

	def get_tablename(self, name, namespace=None):
		tablename = f'{name}'
		if namespace:
			tablename += f'_{namespace}'
		return tablename

	def create_table(self, tablename):
		stmt = f'''
		CREATE TABLE IF NOT EXISTS {tablename}
		(
		key STRING,
		val VARIANT
		)
		'''
		self.connection.execute(stmt)

	@property
	def session(self):
		if self._session:
			return self._session
		else:
			Session = sessionmaker()
			Session.configure(bind=self.engine)
			self._session = Session()
			return self._session

	@property
	def connection(self):
		if self._connection:
			return self._connection
		else:
			self._connection = self.engine.connect()
			return self._connection

	def set(self, key, val):
		item = self._get(key)
		if item.first():
			print('has val')
			item.val = val
			self.session.commit()
		else:
			print('creating val')
			item = self.KeyVal(key=key, val=val)
			self.session.add(item)
			self.session.commit()

	def _get(self, key):
		val = self.session.query(self.KeyVal).filter(
			self.KeyVal.key==key
		)
		return val

	def get(self, key):
		return self._get(key).first().val

	def delete(self, key):
		val = self._get(key)
		val.delete()
		self.session.commit()

	def clear(self):
		self.session.query(self.KeyVal).delete()
		self.session.commit()