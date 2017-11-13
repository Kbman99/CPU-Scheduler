from enum import Enum


class State(Enum):
    """
    Global enum states for the program

    :param EXECUTING: process state to indicate process is currently executing on the CPU
    :param READY: process state to indicate process is currently ready and waiting to run on the CPU
    :param IO: process state to indicate process is currently in IO
    :param STOPPED: process state to indicate process is currently stopped and has completed all IO and CPU

    :param RUNNING: main loop state to indicate loop should continue to run
    :param COMPLETE: main loop state to indicate loop should exit
    """
    EXECUTING = 0
    READY = 1
    IO = 2
    STOPPED = 3
    # For CPU loop
    RUNNING = 4
    COMPLETE = 5
