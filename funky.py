from collections import deque
import bisect


class FunkyDeque(deque):
    def _insert(self, index, process):
        self.rotate(-index)
        self.appendleft(process)
        self.rotate(index)

    def insert(self, process):
        self._insert(bisect.bisect_left(self, process), process)

    def __init__(self, iterable):
        super(FunkyDeque, self).__init__(sorted(iterable))

    def extend(self, iterable):
        for item in iterable:
            self.insert(item)
