from collections import deque
from printupdate import update_mlfq as update
from process import Process
from state import State
from process import tq_dict


def find_lowest_io(io):
    """
    Finds the process with the lowest IO time remaining from within the io_queue

    :param io: io_queue containing all process in State.IO
    :return: Lowest io time
    """
    lowest_io = 999
    for p in io:
        if p.current_io < lowest_io:
            lowest_io = p.current_io
    return lowest_io


def check_empty(queue):
    """
    Check if the main queue for MLFQ is empty

    :param queue: List of queues
    :return: True if empty, False if contains item
    """
    for q in queue:
        if q:
            return False
    return True


def pop_left_mlfq(queue):
    """
    Same as pop_left for a deque() object, but works for a list of deque() objects

    :param queue: The main queue containing all processes in State.READY
    :return: Next process in the queue
    """
    for q in queue:
        if q:
            return q.popleft()


def higher_priority_check(current_p, p):
    """
    Checks if priority of current_p is higher or lower than p

    :param current_p: The current process
    :param p: Process to compare against
    :return: True if current_p has higher priority, False otherwise
    """
    if current_p is None:
        return False
    if current_p.tq_tier > p.tq_tier:
        return True
    return False


status = State.RUNNING

ready_queue_1 = deque()
ready_queue_2 = deque()
ready_queue_3 = deque()

main_queue = [ready_queue_1, ready_queue_2, ready_queue_3]

io_processes = []

P1 = Process([4, 5, 6, 7, 6, 4, 5, 4], [15, 31, 26, 24, 41, 51, 16, 0], name="P1", tq=True)
P2 = Process([9, 11, 15, 12, 8, 11, 9, 10, 7], [28, 22, 21, 28, 34, 34, 29, 31, 0], name="P2", tq=True)
P3 = Process([24, 12, 6, 17, 11, 22, 18], [28, 21, 27, 21, 54, 31, 0], name="P3", tq=True)
P4 = Process([15, 14, 16, 18, 14, 13, 16, 15], [35, 41, 45, 51, 61, 54, 61, 0], name="P4", tq=True)
P5 = Process([6, 5, 15, 4, 7, 4, 6, 10, 3], [22, 21, 31, 26, 31, 18, 21, 33, 0], name="P5", tq=True)
P6 = Process([22, 27, 25, 11, 19, 18, 6, 6], [38, 41, 29, 26, 32, 22, 26, 0], name="P6", tq=True)
P7 = Process([4, 7, 6, 5, 4, 7, 6, 5, 6, 9], [36, 31, 32, 41, 42, 39, 33, 34, 21, 0], name="P7", tq=True)
P8 = Process([5, 4, 6, 4, 6, 5, 4, 6, 6], [14, 33, 31, 31, 27, 21, 19, 11, 0], name="P8", tq=True)

process_list = [P1, P2, P3, P4, P5, P6, P7, P8]
ready_queue_1.extend(process_list)

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
        if check_empty(main_queue) and io_queue:
            current_process = None
            idle_time += 1
            if idle:
                update(clock, current_process, main_queue, io_queue, stopped, first_idle=True)
                idle = 0
        else:
            lowest_io = 0
            idle = 0
            current_process = pop_left_mlfq(main_queue)
            current_process.state = State.EXECUTING
            current_process.set_arrival(clock)
            update(clock, current_process, main_queue, io_queue, stopped)
    for process in process_list:
        if process.state is State.EXECUTING:
            process.current_burst -= 1
            process.tq_length -= 1
            if process.current_burst <= 0:
                # Add completion time and reset the time quantum length of the respective process
                process.completion_times.append(clock)
                process.tq_length = tq_dict[process.tq_tier]
                if process.current_io != 0:
                    process.state = State.IO
                    io_queue.append(process)
                else:
                    process.state = State.STOPPED
                    stopped.append(process.name)
                    process.set_tat()
                current_process = None
            elif process.tq_length <= 0:
                # Set the time quantum to the next tier and place process in the proper
                # ready queue based on it's time quantum
                process.state = State.READY
                process.set_next_tq()
                main_queue[process.tq_tier - 1].append(process)
                current_process = None
        elif process.state is State.IO:
            process.current_io -= 1
            if process.current_io <= 0:
                io_queue.remove(process)
                process.state = State.READY
                process.set_burst_io()
                if process.state is not State.STOPPED:
                    main_queue[process.tq_tier - 1].append(process)
                if higher_priority_check(current_process, process):
                    # Reset the tq_length back to what it should be based on it's tq_tier
                    # and add back to the main_queue
                    current_process.state = State.READY
                    current_process.tq_length = tq_dict[current_process.tq_tier]
                    main_queue[current_process.tq_tier - 1].append(current_process)
                    current_process = None
        elif process.state is State.READY:
            process.waiting_time += 1

    clock += 1

    if not current_process and not idle and check_empty(main_queue):
        if find_lowest_io(io_queue) > lowest_io:
            # A check to see if the process has been idle or not
            lowest_io = find_lowest_io(io_queue)
            idle = 1

    if check_empty(main_queue) and not current_process and not io_queue:
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
print("CPU Utilization:    {:%}\n".format((clock-idle_time)/clock))
print("Waiting Times       P1    P2    P3    P4    P5    P6    P7    P8")
print("                    {:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}".format(*wt_list))
print("Average Wait:       {}\n".format(sum(wt_list)/8))
print("Turnaround Times    P1    P2    P3    P4    P5    P6    P7    P8")
print("                    {:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}".format(*tat_list))
print("Average Turnaround: {}\n".format(sum(tat_list) / 8))
print("Response Times      P1    P2    P3    P4    P5    P6    P7    P8")
print("                    {:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}".format(*rt_list))
print("Average Response:   {}\n".format(sum(rt_list) / 8))
