# PyKeyVal
> Heavily inspired by [`keyv`](https://github.com/lukechilds/keyv)
![CircleCI](https://circleci.com/gh/tchoedak/PyKeyVal.svg?style=shield)

PyKeyVal is a key-value store that you can pack in a bag and take with you.

# Installation

To install PyKeyVal, simply:
`pip install pykeyval`

or from source:
`python setup.py install`

# Getting Started

```python
>>> import pykeyval
>>> kv = pykeyval.PyKeyVal(url='sqlite:///opt/myapp/db.sqlite')
>>> kv.set('key', 'val')
True
>>> kv.get('key')
'val'
```

# API

## get(key)
Returns the value set for key `key`.

## set(key, val)
Sets the key `key` to a value `val`. Returns True.

## delete(key)
Deletes the key `key`. Returns True if the key existed.

## clear()
Deletes all keys in the current name and namespace. Returns True.

# Storage Backends

PyKeyVal supports the following backends:

| Database   |  Interface  | Required Arguments | Options   |
|------------|:-----------:|--------------------|-----------|
| Memory     |             |                    |           |
| File       |             | name               | path      |
| Redis      |             | url, name          | namespace |
| Snowflake  |             | url, name          | namespace |
| SQLite     |             | url, name          | namespace |
| PostgreSQL | Coming soon |                    |           |
| MySQL      | Coming soon |                    |           |

# Namespaces

PyKeyVal allows you to setup namespaces for database backends to prevent key collisions.

# Serializers

PyKeyVal uses python's builtin `json` lib to perform data serialization across multiple backends for data consistency.

You can hook up your own serializer by passing in a serializer class that implements `serialize` and `deserialize`:
```python
class PickleSerializer:
    def serialize(data):
        pickle.dumps(data)
    def deserialize(data):
        pickel.loads(data)

kv = PyKeyVal(serializer=PickleSerializer)
```
