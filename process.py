from collections import deque
import functools
from state import State

tq_dict = {
    1: 6,
    2: 12,
    3: 999
}


@functools.total_ordering
class Process:
    def __init__(self, burst_times, io_times, name, state=State.READY, arrival_time=0, tq=False):
        self.burst_times = deque(burst_times)
        self.io_times = deque(io_times)
        self.current_burst = self.burst_times.popleft()
        self.current_io = self.io_times.popleft()
        self.state = state
        self.next_arrival_time = arrival_time
        self.burst_time = sum(burst_times)
        self.completion_times = []
        self.arrival_times = []
        self.tat = 0
        self.name = name
        self.waiting_time = 0
        if tq:
            self.tq_tier = 1
            self.tq_length = tq_dict[1]

    def __lt__(self, other):
        return self.next_arrival_time < other.next_arrival_time

    def __eq__(self, other):
        return self.next_arrival_time == other.next_arrival_time

    def __name__(self):
        return self.__name__()

    def set_arrival(self, current_time):
        """
        Runs as the process enters the executing state

        Set the arrival time based on the current time in the loop
        and current CPU burst + IO times as well as appending the arrival
        time and current time to a list for use in later calculations upon completion

        :param current_time: The current time in the loop
        :return:
        """
        self.next_arrival_time = current_time + self.current_burst + self.current_io
        self.arrival_times.append(self.next_arrival_time)

    def set_burst_io(self):
        """
        Runs once the process IO time hits 0 or enters the waiting/ready state

        Sets the current CPU burst and IO times to the next in the list

        :return:
        """
        try:
            self.current_burst = self.burst_times.popleft()
            self.current_io = self.io_times.popleft()
        except IndexError:
            self.state = State.STOPPED

    def set_tat(self):
        """
        Runs upon completion of the process

        Sets the Turn Around Time for the given process

        :return:
        """
        self.tat = self.waiting_time + self.burst_time

    def set_next_tq(self):
        """
        MLFQ ONLY- Runs if the process time quantum goes below 0
        :return:
        """
        if self.tq_tier != 3:
            self.tq_tier += 1
            self.tq_length = tq_dict[self.tq_tier]
