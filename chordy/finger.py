from .constants import K


class Finger(object):

    def __init__(self, uid, i):
        self.start = (uid + 2**i) % K
        self.node = None
