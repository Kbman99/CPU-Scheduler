from enum import Enum


class State(Enum):
    EXECUTING = 0
    READY = 1
    IO = 2
    STOPPED = 3
    # For CPU loop
    RUNNING = 4
    COMPLETE = 5
