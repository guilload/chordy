import socket

from .base import Base


class Node(Base):
    def __init__(self, address, predecessor=None, successor=None):
        super(Node, self).__init__(address)

        self.predecessor = Node(predecessor) if predecessor else None
        self.successor = Node(successor) if successor else None

    def fire(self, rpc):  # fire and forget
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        rpc['forget'] = True
        sock.sendall(self.encode(rpc))

        sock.close()

    def send(self, rpc):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.sendall(self.encode(rpc))

        data = sock.recv(4096)
        sock.close()
        return self.decode(data)

    def find_successor(self, uid):
        rpc = {'method': 'find_successor', 'uid': uid}
        return self.send(rpc)

    def closest_preceding_finger(self, uid):
        rpc = {'method': 'closest_preceding_finger', 'uid': uid}
        return self.send(rpc)

    def update_fingers(self, node, i):
        rpc = {'method': 'update_fingers', 'node': node, 'i': i}
        self.fire(rpc)

    def update_predecessor(self, node):
        rpc = {'method': 'update_predecessor', 'node': node}
        self.fire(rpc)
