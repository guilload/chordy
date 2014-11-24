import asyncio
import hashlib
import json
import logging
import sys

from constants import m
from finger import Finger
from interval import Interval


LOGGER = logging.getLogger(__name__)


class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.uid = self.hsh(self.endpoint)
        self.fingers = [Finger(self.uid, i) for i in range(1, m + 1)]

        self.predecessor = None
        self.successor = None

    @property
    def endpoint(self):
        return '{}:{}'.format(self.host, self.port)

    def join(self, seed):
        if seed:
            self.init_fingers(seed)
            self.update_others()
            self.relocate_keys()
            #  move keys in (predecessor, n] from successor

        else:  # only node in the network
            self.predecessor = self
            self.successor = self

            for finger in self.fingers:
                finger.node = self

    def init_fingers(self, seed):
        node = Node(seed)

        self.fingers[0] = node.find_successor(self.fingers[0].start)
        self.predecessor = self.successor.predecessor
        self.successor.predecessor = self

        for fingerj, fingeri in zip(self.fingers[1:], self.fingers[:-1]):
            if fingerj.start in Interval(self.uid, fingeri.node.uid, rexclude=True):
                fingerj.node = fingeri.node
            else:
                fingerj.node = node.find_successor(fingerj.start)

    def update_others(self):
        for i in range(m):
            p = self.find_predecessor(self.uid - 2**i)
            p.update_fingers(self.uid, i)

    def update_fingers(self, s, i):
        if s in Interval(self.uid, self.fingers[i].node.uid):
            self.fingers[i].node = s
            self.predecessor.update_fingers(s, i)

    def relocate_keys():
        pass

    def handle(self, key):
        uid = self.hsh(key)
        return self.find_successor(uid)

    def find_successor(self, uid):
        predecessor = self.find_predecessor(uid)
        return predecessor.successor.endpoint

    def find_predecessor(self, uid):
        node = self

        while node.uid not in Interval(node.uid, node.successor.uid, lexclude=True):
            node = node.closest_preceding_finger(uid)
        return node

    def hsh(self, key):
        return int(hashlib.sha256(key.encode('ascii')).hexdigest(), 16)


class ServerProtocol(asyncio.Protocol):

    def __init__(self, server):
        self.server = server
        self.transport = None

    @staticmethod
    def decode(data):
        return json.loads(data.decode())

    @staticmethod
    def encode(data):
        return json.dumps(data).encode()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        request = self.decode(data)
        response = self.server.handle(request)

        if response:
            self.transport.write(self.encode(response))


def run(port, seed=None):
    loop = asyncio.get_event_loop()
    chord = Server('localhost', port, seed)
    coroutine = loop.create_server(lambda: ServerProtocol(chord), 'localhost', port)
    server = loop.run_until_complete(coroutine)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    port = int(sys.argv[1])
    seed = sys.argv[2] if len(sys.argv >= 3) else None
    run(port, seed)
