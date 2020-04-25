# Tal Bachar
# CSCI 340
# Home Project
# Prof. Pavel Shostak

import sys
################################################################################
class Process:
    def __init__(self, pid, realtime, bytes, using_cpu, got_preempted):
        self.pid = pid
        if realtime == True:
            self.realtime = "Realtime"
        else:
            self.realtime = "Common"
        self.bytes = bytes
        self.using_cpu = using_cpu
        self.got_preempted = got_preempted

################################################################################
def computer_specs():
    #RAM memory
    RAM_memory = int(input("\n\n\tPlease enter amount of RAM memory on simulated computer: "))
    while RAM_memory < 1 or RAM_memory > 4000000000:
        RAM_memory = int(input("\n\n\tRAM memory must be a positive number, less than or equal to 4 billion: "))

    #HDD
    num_of_harddisk = int(input("\n\n\tPlease enter amount of hard disks on simulated computer: "))
    while num_of_harddisk < 1:
        num_of_harddisk = int(input("\n\n\tAmount of hard disks must be greater than 0: "))

    return RAM_memory, num_of_harddisk;

################################################################################
def preempt(ready_queue):
    for process in ready_queue:
        if process.using_cpu == True:
            process.using_cpu = False
            process.got_preempted = True

##################################################################
def print_Sr(ready_queue):

    print("\tPID\t  TYPE\t\tSTATUS")
    print("\t--------------------------------")
        #Check if there is a running program, and if so print it first
    for p in ready_queue:
        if p.using_cpu == True:
            print("\t", p.pid, "\t", p.realtime, "\t", "Running")

    #Then check if there are preempted RT processes in the ready_queue, print them
    for p in ready_queue:
        if p.using_cpu == False and p.realtime == "Realtime" and p.got_preempted == True:
            print("\t", p.pid, "\t", p.realtime, "\t", "Waiting")

    #After, check if there are RT processes that were not preempted
    for p in ready_queue:
        if p.using_cpu == False and p.realtime == "Realtime" and p.got_preempted == False:
            print("\t", p.pid, "\t", p.realtime, "\t", "Waiting")

    #Check if there are any common preempted processes in the ready_queue
    for p in ready_queue:
        if p.realtime == "Common" and p.got_preempted == True:
            print("\t", p.pid, "\t", p.realtime, "\t", "Waiting <--- Got Preempted")

    #Print rest of preocesses
    for p in ready_queue:
        if p.using_cpu == False and p.got_preempted == False and p.realtime == "Common":
            print("\t", p.pid, "\t", p.realtime, "\t", "Waiting")

################################################################################
def print_Sm(ready_queue):

    print("\tPID\t  MEM_START\tMEM_END")
    print("\t--------------------------------")

    RAM_start = 0

    #Check if there is a running program, and if so print it first
    for p in ready_queue:
        if p.using_cpu == True:
            print("\t", p.pid, "\t", RAM_start, "\t\t", RAM_start+p.bytes-1)
            RAM_start += p.bytes

    #Check if there are any preempted processes in the ready_queue
    for p in ready_queue:
        if p.got_preempted == True:
            print("\t", p.pid, "\t", RAM_start, "\t\t", RAM_start+p.bytes-1)
            RAM_start += p.bytes

    for p in ready_queue:
        if p.using_cpu == False and p.got_preempted == False:
            print("\t", p.pid, "\t", RAM_start, "\t\t", RAM_start+p.bytes-1)
            RAM_start += p.bytes

################################################################################
def timeSliceEnded(ready_queue, current_process):

    chooseNext(ready_queue, current_process)

################################################################################

def chooseNext(ready_queue, current_process):
    current_process.using_cpu = False

    for p in ready_queue:
        if p.got_preempted == True and p.realtime == "Realtime" and p != current_process: #RT process that got preempted starts running
            p.using_cpu = True
            p.got_preempted = False
            return False

    for p in ready_queue:
        if p.realtime == "Realtime" and p != current_process: #RT process waiting starts running
            p.using_cpu = True
            return False

    for p in ready_queue:
        if p.got_preempted == True  and p != current_process: #Common process that got preempted starts running
            p.using_cpu = True
            p.got_preempted = False
            return False

    for p in ready_queue:
        if p.using_cpu == False and p.got_preempted == False and p.realtime == "Common" and p != current_process:
            p.using_cpu = True
            break

################################################################################

def terminate_process(ready_queue, current_process):

    chooseNext(ready_queue, current_process)
    ready_queue.remove(current_process)

################################################################################

def main():
    RAM_memory, num_of_harddisk = computer_specs()

    ready_queue = []
    pid = 0

    while True:

        using_cpu = False
        user_input = str(input(""))

        #Add common process
        if user_input.split()[0] == "A":
            pid += 1
            if (not ready_queue):
                using_cpu = True

            new_common_process = Process(pid, False, int(user_input.split()[1]), using_cpu, False)
            ready_queue.append(new_common_process)

        #Add realtime process
        elif user_input.split()[0] == "AR":
            pid += 1
            using_cpu = True
            if (ready_queue):   #if there are processes in RQ or in CPU
                preempt(ready_queue)   #preempt CPU-using processes, set got_preempted=True

            new_rt_process = Process(pid, True, int(user_input.split()[1]), using_cpu, False)
            ready_queue.append(new_rt_process)


        elif user_input.split()[0] == "S":
            if user_input.split()[1] == "r":
                print_Sr(ready_queue)

            elif user_input.split()[1] == "m":
                print_Sm(ready_queue)

        elif user_input == "Q":
            for p in ready_queue:
                if p.using_cpu == True:
                    current_process = p
                    break
            timeSliceEnded(ready_queue, current_process)

        elif user_input == "t":
            for p in ready_queue:
                if p.using_cpu == True:
                    current_process = p
                    break
            terminate_process(ready_queue, current_process)

        elif user_input == "quit":
            sys.exit(0)


################################################################################


main()
