import socket
import sys

from .base import Base
from .constants import K, m
from .finger import Finger
from .interval import Interval
from .node import Node


class Server(Base):
    def __init__(self, address):
        super(Server, self).__init__(address)

        self.fingers = [Finger(self.uid, i) for i in range(m)]
        self.predecessor = None

    @property
    def successor(self):
        return self.fingers[0].node

    @successor.setter
    def successor(self, node):
        self.fingers[0].node = node

    def join(self, seed=None):
        if seed:
            self.init_fingers(seed)
            self.update_others()
            #  move keys in (predecessor, n] from successor

        else:  # only node in the network
            self.predecessor = self

            for finger in self.fingers:
                finger.node = self

        self.run()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))

        while True:
            sock.listen(5)

            conn, _ = sock.accept()
            data = conn.recv(4096)
            rpc = self.decode(data)

            forget = rpc.pop('forget', False)

            if forget:
                conn.close()

            method = rpc.pop('method')
            res = getattr(self, method)(**rpc)

            if forget:
                continue

            conn.sendall(self.encode(res))
            conn.close()

    def init_fingers(self, seed):
        self.successor = seed.find_successor(self.fingers[0].start)
        self.predecessor = self.successor.predecessor
        self.successor.update_predecessor(self)

        for fingerj, fingeri in zip(self.fingers[1:], self.fingers[:-1]):

            if fingerj.start in Interval(self.uid, fingeri.node.uid, rexclude=True):
                fingerj.node = fingeri.node
            else:
                fingerj.node = seed.find_successor(fingerj.start)

    def update_others(self):
        for i in range(m):
            node = self.find_predecessor((self.uid - 2**i) % K)
            node.update_fingers(self, i)

    def update_fingers(self, node, i):
        if node.uid in Interval(self.uid, self.fingers[i].node.uid, rexclude=True):
            self.fingers[i].node = node
            self.predecessor.update_fingers(node, i)

    def update_predecessor(self, node):
        self.predecessor = node

    def find_successor(self, uid):
        predecessor = self.find_predecessor(uid)
        return predecessor.successor

    def find_predecessor(self, uid):
        node = self

        while uid not in Interval(node.uid, node.successor.uid, lexclude=True):
            node = node.closest_preceding_finger(uid)

        return node

    def closest_preceding_finger(self, uid):
        for finger in reversed(self.fingers):
            if finger.node.uid in Interval(self.uid, uid, lexclude=True, rexclude=True):
                return finger.node

        return self


if __name__ == '__main__':
    address = sys.argv[1]
    seed = Node(sys.argv[2]) if len(sys.argv) >= 3 else None
    Server(address).join(seed)
