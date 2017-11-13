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


def update_fcfs(clock, current_process, ready_queue, io_queue, stopped, first_idle=False):
    """
    Updates the context switch on screen to display relevant data

    :param clock:
    :param current_process: Currently executing process
    :param ready_queue: All process in READY state
    :param io_queue: All processes in IO state
    :param stopped: All processes in STOPPED state
    :param first_idle: Set if
    :return:
    """
    print("\nCurrent Time: {}".format(clock))
    if not first_idle:
        print("\nCurrent Process: {}".format(current_process.name))
    else:
        print("\nCurrent Process: idle")
    print("\n---------------------------------------------------")
    print("\nReady Queue:   Process    Burst")
    if not ready_queue:
        print("               None")
    else:
        for process in ready_queue:
            print("               {}        {}".format(process.name, process.current_burst))
    print("\n---------------------------------------------------")
    print("\nI/O Queue:     Process    Remaining I/O Time")
    if not io_queue:
        print("               None")
    else:
        for process in io_queue:
            print("               {}         {}".format(process.name, process.current_io))
    if stopped:
        print("\n---------------------------------------------------")
        print("Completed:     ", end="")
        print(*stopped, sep=",  ")
    print("\n---------------------------------------------------")
    print("---------------------------------------------------")


def update_mlfq(clock, current_process, main_queue, io_queue, stopped, first_idle=False):
    """
    Updates the context switch on screen to display relevant data

    :param clock:
    :param current_process: Currently executing process
    :param main_queue: All process in READY state
    :param io_queue: All processes in IO state
    :param stopped: All processes in STOPPED state
    :param first_idle: Set if
    :return:
    """
    print("\nCurrent Time: {}".format(clock))
    if not first_idle:
        print("\nCurrent Process: {}".format(current_process.name))
    else:
        print("\nCurrent Process: idle")
    print("\n---------------------------------------------------")
    print("\nReady Queue:   Process    Burst    Queue")
    if check_empty(main_queue):
        print("               None")
    else:
        for q in main_queue:
            for process in q:
                print("               {}         {:<8} Q{}".format(process.name, process.current_burst, process.tq_tier))
    print("\n---------------------------------------------------")
    print("\nI/O Queue:     Process    Remaining I/O Time")
    if not io_queue:
        print("               None")
    else:
        for process in io_queue:
            print("               {}         {}".format(process.name, process.current_io))
    if stopped:
        print("\n---------------------------------------------------")
        print("Completed:     ", end="")
        print(*stopped, sep=",  ")
    print("\n---------------------------------------------------")
    print("---------------------------------------------------")
