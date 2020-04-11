'''
Implements a KeyVal Store where a local file is the backend
'''
import json
import os


class FileKeyVal(object):
    def __init__(self, name, **options):
        self.options = options
        self.filename = f'.pykeyval_{name}'
        self.path = options.get('path') or self.filename

    def _read(self):
        with open(self.path, 'r') as f:
            data = f.read()
            if data:
                return json.loads(data)
            else:
                return dict()

    def _write(self, data):
        with open(self.path, 'w') as f:
            f.write(json.dumps(data))

    def get(self, key):
        data = self._read()
        return data.get(key)

    def set(self, key, val):
        if os.path.isfile(self.path):
            data = self._read()
        else:
            data = dict()

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
        open(self.path, 'w').close()
        return True
