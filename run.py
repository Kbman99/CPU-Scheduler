from MLQ import mlfq
from FCFS import firstcomefirstserve

if __name__ == "__main__":
    while True:
        option = input("Please type 'mlfq' or `fcfs` to run the respective program: ")
        option.lower()

        if option == 'mlfq':
            mlfq.run_mlfq()
            print("\n\nThe simulation has ended. Follow the prompt below to run again.\n")
        elif option == 'fcfs':
            firstcomefirstserve.run_fcfs()
            print("\n\nThe simulation has ended. Follow the prompt below to run again.\n")
        else:
            print("You've entered the wrong option. Please type either 'mlfq' or 'fcfs'\n")
