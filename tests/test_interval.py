from chordy.interval import Interval


class TestInverval(object):

    def test_interval(self):
        interval = Interval(0, 2)

        assert 0 in interval
        assert 1 in interval
        assert 2 in interval

        assert 3 not in interval

    def test_lexclude(self):
        assert 0 not in Interval(0, 2, lexclude=True)

    def test_rexclude(self):
        assert 2 not in Interval(0, 2, rexclude=True)

    def test_reverse(self):
        interval = Interval(4, 2)

        assert 4 in interval
        assert 5 in interval
        assert 0 in interval
        assert 1 in interval
        assert 2 in interval

        assert 3 not in interval

    def test_reverse_lexclude(self):
        interval = Interval(4, 2, lexclude=True)

        assert 4 not in interval

        assert 5 in interval
        assert 0 in interval
        assert 1 in interval
        assert 2 in interval

        assert 3 not in interval

    def test_reverse_rexclude(self):
        interval = Interval(4, 2, rexclude=True)

        assert 4 in interval
        assert 5 in interval
        assert 0 in interval
        assert 1 in interval

        assert 2 not in interval

        assert 3 not in interval

    def test_empty(self):
        assert 0 in Interval(0, 0)
        assert 0 in Interval(0, 0, lexclude=True)
        assert 0 in Interval(0, 0, rexclude=True)

        assert 0 not in Interval(0, 0, lexclude=True, rexclude=True)
