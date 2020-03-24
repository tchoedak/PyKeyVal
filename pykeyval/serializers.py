import json


class JsonSerializer(object):
    def serialize(value_items):
        return json.dumps(value_items)

    def deserialize(value_items):
        return json.loads(value_items)
