import pytest
from pykeyval import PyKeyVal


@pytest.fixture
def dict_kv():
	kv = PyKeyVal(store='dict')
	return kv

@pytest.fixture
def file_kv():
	kv = PyKeyVal(name='fkv_test', path='/tmp/fkv_test', store='file')
	return kv

@pytest.fixture
def sqlite_kv():
	kv = PyKeyVal(url='sqlite:////tmp/.pykevval.sqlite', name='mykeyv')
	return kv

@pytest.fixture
def sqlite_memory_kv():
	kv = PyKeyVal(url='sqlite:///:memory:', name='memkv', namespace='memkvtest')
	return kv

@pytest.fixture
def local_kvs(dict_kv, file_kv, sqlite_kv, sqlite_memory_kv):
	return [dict_kv, file_kv, sqlite_kv, sqlite_memory_kv]

def test_pkv_api(local_kvs):
	'''
	Test all PyKeyVal operations
	'''
	key, val = 'testkey', 'testval'

	for kv in local_kvs:
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
