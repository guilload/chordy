from operator import le, lt


class Interval(object):
    """
    >>> 1 in Interval(0, 2)
    True
    >>> 0 in Interval(0, 2)
    True
    >>> 0 in Interval(0, 2, lexclude=True)
    False
    >>> 2 in Interval(0, 2, rexclude=True)
    False
    >>> 0 in Interval(5, 2)
    True
    """

    def __init__(self, start, end, lexclude=False, rexclude=False):
        self.start = start
        self.end = end
        self.lexclude = lexclude
        self.rexclude = rexclude

    def operators(self, swap=False):
        if swap:
            return (le if self.lexclude else lt, le if self.rexclude else lt)
        else:
            return (lt if self.lexclude else le, lt if self.rexclude else le)

    def __contains__(self, value):
        if self.start < self.end:
            left, right = self.operators()
            return left(self.start, value) and right(value, self.end)
        else:
            left, right = self.operators(swap=True)
            return not (left(value, self.start) and right(self.end, value))
