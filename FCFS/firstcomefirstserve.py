from collections import deque
from printupdate import update_fcfs as update
from process import Process
from state import State


def find_lowest_io(io):
    """
    Check if the main queue for MLFQ is empty
    :param io: List of queues
    :return: True if empty, False if contains item
    """
    lowest_io = 999
    for p in io:
        if p.current_io < lowest_io:
            lowest_io = p.current_io
    return lowest_io


def run_fcfs():
    status = State.RUNNING

    ready_queue = deque()

    P1 = Process([4, 5, 6, 7, 6, 4, 5, 4], [15, 31, 26, 24, 41, 51, 16, 0], name="P1")
    P2 = Process([9, 11, 15, 12, 8, 11, 9, 10, 7], [28, 22, 21, 28, 34, 34, 29, 31, 0], name="P2")
    P3 = Process([24, 12, 6, 17, 11, 22, 18], [28, 21, 27, 21, 54, 31, 0], name="P3")
    P4 = Process([15, 14, 16, 18, 14, 13, 16, 15], [35, 41, 45, 51, 61, 54, 61, 0], name="P4")
    P5 = Process([6, 5, 15, 4, 7, 4, 6, 10, 3], [22, 21, 31, 26, 31, 18, 21, 33, 0], name="P5")
    P6 = Process([22, 27, 25, 11, 19, 18, 6, 6], [38, 41, 29, 26, 32, 22, 26, 0], name="P6")
    P7 = Process([4, 7, 6, 5, 4, 7, 6, 5, 6, 9], [36, 31, 32, 41, 42, 39, 33, 34, 21, 0], name="P7")
    P8 = Process([5, 4, 6, 4, 6, 5, 4, 6, 6], [14, 33, 31, 31, 27, 21, 19, 11, 0], name="P8")

    process_list = [P1, P2, P3, P4, P5, P6, P7, P8]
    ready_queue.extend(process_list)

    io_queue = []
    stopped = []

    idle_time = 0
    clock = 0
    idle = 0
    current_process = None
    lowest_io = 0

    while status is State.RUNNING:
        # If loop has just begun, assign new process to CPU and set arrival times
        if clock == 0 or current_process is None:
            if not ready_queue and io_queue:
                current_process = None
                idle_time += 1
                if idle:
                    # Print update on context switch if first clock of being idle
                    update(clock, current_process, ready_queue, io_queue, stopped, first_idle=True)
                    idle = 0
            else:
                # Reset lowest IO to ensure we don't reprint the context of an idle process which
                # has already been printed to screen
                lowest_io = 0
                idle = 0
                current_process = ready_queue.popleft()
                current_process.state = State.EXECUTING
                current_process.set_arrival(clock)
                # Print update on context switch
                update(clock, current_process, ready_queue, io_queue, stopped)

        for process in process_list:
            if process.state is State.EXECUTING:
                process.current_burst -= 1
                if process.current_burst <= 0:
                    process.completion_times.append(clock)
                    # Ensure there is IO to be done, if not then set State of process to STOPPED
                    if process.current_io != 0:
                        process.state = State.IO
                        io_queue.append(process)
                        process.current_io -= 1
                    else:
                        process.state = State.STOPPED
                        stopped.append(process.name)
                        process.set_tat()
                    current_process = None
            elif process.state is State.IO:
                # Check if there is IO to be done, if not then remove the process and set State of process
                # to READY
                if process.current_io <= 0:
                    io_queue.remove(process)
                    process.state = State.READY
                    process.set_burst_io()
                    # Ensure process is not State STOPPED
                    if process.state is not State.STOPPED:
                        ready_queue.append(process)
                else:
                    process.current_io -= 1
            elif process.state is State.READY:
                process.waiting_time += 1

        clock += 1

        if not current_process and not idle and not ready_queue:
            if find_lowest_io(io_queue) > lowest_io:
                # A check to see if the process has been idle or not
                lowest_io = find_lowest_io(io_queue)
                idle = 1

        # Check if we are done with all processes
        if not ready_queue and not current_process and not io_queue:
            status = State.COMPLETE

    tat_list = []
    rt_list = []
    wt_list = []

    for process in process_list:
        tat_list.append(process.tat)
        rt_list.append(process.response_time)
        wt_list.append(process.waiting_time)

    print("Complete!\n")
    print("Total Time:         {}".format(clock))
    print("CPU Utilization:    {:%}".format((clock-idle_time)/clock))
    print("Waiting Times       P1    P2    P3    P4    P5    P6    P7    P8")
    print("                    {:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}".format(*wt_list))
    print("Average Wait:       {}\n".format(sum(wt_list)/8))
    print("Turnaround Times    P1    P2    P3    P4    P5    P6    P7    P8")
    print("                    {:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}".format(*tat_list))
    print("Average Turnaround: {}\n".format(sum(tat_list) / 8))
    print("Response Times      P1    P2    P3    P4    P5    P6    P7    P8")
    print("                    {:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}".format(*rt_list))
    print("Average Response:   {}".format(sum(rt_list) / 8))
