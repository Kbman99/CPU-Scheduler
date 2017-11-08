def update(clock, current_process, ready_queue, io_queue):
    print("\nCurrent Time: {}".format(clock))
    print("\nCurrent Process: {}".format(current_process.name))
    print("\n---------------------------------------------------")
    print("\nReady Queue:   Process    Burst")
    if not ready_queue:
        print("               None")
    else:
        for process in ready_queue:
            print("               {}        {}".format(process.name, process.current_burst))
    print("\n---------------------------------------------------")
    print("\nI/O Queue:    Process    Remaining I/O Time")
    if not io_queue:
        print("              None")
    else:
        for process in io_queue:
            print("              {}         {}".format(process.name, process.current_io))
    print("\n---------------------------------------------------")
    print("---------------------------------------------------")
