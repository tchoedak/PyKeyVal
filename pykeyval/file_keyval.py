'''
Implements a KeyVal Store where a local file is the backend
'''
import json


class FileKeyVal(object):
    def __init__(self, name, **options):
        self.options = options
        self.filename = f'.pykeyval_{name}'

    def _read(self):
        with open(self.filename, 'r') as f:
            data = f.read()
            if data:
                return json.loads(data)
            else:
                return dict()

    def _write(self, data):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(data))

    def get(self, key):
        data = json.loads(self._read())
        return data.get(key)

    def set(self, key, val):
        data = self._read()
        data[key] = val
        self._write(data)
        return True

    def delete(self, key):
        data = self._read()
        if key in data.keys():
            del data[key]
            self._write(data)
            return True
        return False

    def clear(self):
        open(self.filename, 'w').close()
        return True
