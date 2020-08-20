import os
import pytest
from pykeyval import PyKeyVal


@pytest.fixture
def snow_kv():
	user = os.environ.get('SNOWFLAKE_USERNAME')
	password = os.environ.get('SNOWFLAKE_PASSWORD')
	account = os.environ.get('SNOWFLAKE_ACCOUNT')
	database = os.environ.get('SNOWFLAKE_DATABASE')
	schema = os.environ.get('SNOWFLAKE_SCHEMA')
	role = os.environ.get('SNOWFLAKE_ROLE')
	warehouse = os.environ.get('SNOWFLAKE_WAREHOUSE')

	SNOW_URL = f'snowflake://{user}:{password}@{account}/{database}/{schema}?drivername=snowflake&role={role}&warehouse={warehouse}'

	kv = PyKeyVal(url=SNOW_URL, name='testkv', namespace='1')
	return kv

@pytest.fixture
def redis_kv():
	url = 'redis://localhost:6379/0'
	kv = PyKeyVal(url=url, name='testkv', namespace='1')
	return kv


@pytest.fixture
def online_kvs(snow_kv, redis_kv):
	return [snow_kv, redis_kv]

def test_online_kvs_api(online_kvs):
	'''
	Test all PyKeyVal operations
	'''
	key, val = 'testkey', 'testval'

	for kv in online_kvs:
		# set/get operation
		kv.set(key, val)
		assert kv.get(key) == val

		# get on keys that don't exist return None
		assert kv.get('nonexistentkey') == None

		# successful delete returns True
		assert kv.delete(key) == True
		# successful delete removes key
		assert kv.get(key) == None

		# unsuccessful delete returns False
		assert kv.delete('nonexistentkey') == False

		# clear removes all keys
		kv.set(key, val)
		kv.set('otherkey', 'otherval')
		kv.clear()
		assert kv.get(key) == None
		assert kv.get('otherkey') == None
