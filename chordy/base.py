import hashlib
import json

from .constants import K


class Encoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Base):
            return {'address': obj.address,
                    'predecessor': obj.predecessor.address if obj.predecessor else None,
                    'successor': obj.successor.address if obj.successor else None,
                    }

        elif isinstance(obj, long):
            return str(obj)

        return json.JSONEncoder.default(self, obj)


class Base(object):
    def __init__(self, address):
        self.address = address
        self.uid = self.hsh(self.address)

    @property
    def host(self):
        host, _ = self.address.split(':')
        return host

    @property
    def port(self):
        _, port = self.address.split(':')
        return int(port)

    @staticmethod
    def hsh(key):
        return int(hashlib.sha1(key).hexdigest(), 16) % K

    def decode(self, data):
        obj = json.loads(data)

        from node import Node  # FIXME

        if 'node' in obj:
            obj['node'] = Node(obj['node'].pop('address'), **obj['node'])

        if 'uid' in obj:
            obj['uid'] = int(obj['uid'])

        if 'address' in obj:
            obj = Node(obj.pop('address'), **obj)

        return obj

    def encode(self, data):
        return json.dumps(data, cls=Encoder)
