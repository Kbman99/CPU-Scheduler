from collections import deque
from printupdate import update
from process import Process
from state import State


status = State.RUNNING

ready_queue = deque()

io_processes = []

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

clock = 0
current_process = None

while status is State.RUNNING:
    # If loop has just begun, assign new process to CPU and set arrival times
    if clock == 0 or current_process is None:
        if not ready_queue and io_queue:
            current_process = None
        else:
            current_process = ready_queue.popleft()
            current_process.state = State.EXECUTING
            current_process.set_arrival(clock)
            update(clock, current_process, ready_queue, io_queue)

    for process in process_list:
        if process.state is State.EXECUTING:
            process.current_burst -= 1
            if process.current_burst <= 0:
                process.completion_times.append(clock)
                if process.current_io != 0:
                    process.state = State.IO
                    io_queue.append(process)
                    process.current_io -= 1
                else:
                    process.state = State.STOPPED
                    process.set_tat()
                current_process = None
        elif process.state is State.IO:
            if process.current_io <= 0:
                io_queue.remove(process)
                process.state = State.READY
                process.set_burst_io()
                if process.state is not State.STOPPED:
                    ready_queue.append(process)
            else:
                process.current_io -= 1
        elif process.state is State.READY:
            process.waiting_time += 1

    clock += 1

    if not ready_queue and not current_process and not io_queue:
        status = State.COMPLETE
        print("We good")


print("DONE")
i = 8
for process in process_list:
    # print("Process {} TaT time is: {}".format(i, process.arrival_times))
    # print("Sum of process {} arrival times are: {}".format(i, process.arrival_times))
    # print("Process {} service times are: {}".format(i, process.service_time))
    # print("Sum of process {} service times are: {}".format(i, process.service_time))
    print("Average wait time for process {} was {} clocks".format(i, process.tat - process.burst_time))
    i -= 1
