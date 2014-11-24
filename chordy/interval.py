class Interval(object):

    def __init__(self, start, end, lexclude=False, rexclude=False):
        self.start = start
        self.end = end
        self.lexclude = lexclude
        self.rexclude = rexclude

    def __contains__(self, value):
        if self.lexclude and self.rexclude:  # ()
            if self.start == self.end:
                res = value != self.start

            elif self.start < self.end:
                res = self.start < value and value < self.end

            else:
                res = value > self.start or value < self.end

        elif self.start == self.end:
            res = True

        elif not self.lexclude and not self.rexclude:  # []
            if self.start < self.end:
                res = self.start <= value and value <= self.end
            else:
                res = value >= self.start or value <= self.end

        elif self.lexclude and not self.rexclude:  # (]
            if self.start < self.end:
                res = self.start < value and value <= self.end
            else:
                res = value > self.start or value <= self.end

        else:  # [)
            if self.start < self.end:
                res = self.start <= value and value < self.end
            else:
                res = value >= self.start or value < self.end

        return res
