'''
Implements a KeyVal Store where the backend is a python dictionary
'''


class DictKeyVal(object):
    def __init__(self, *args, **options):
        self.store = dict()
        self.options = options

    def get(self, key):
        return self.store.get(key)

    def set(self, key, val):
        self.store[key] = val

    def delete(self, key):
        key_exists = self.get(key) is not None
        if key_exists:
            del self.store[key]
        return key_exists

    def clear(self):
        self.store = dict()
        return True
