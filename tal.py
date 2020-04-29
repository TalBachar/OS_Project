# Tal Bachar
# CSCI 340
# Home Project
# Prof. Pavel Shostak

import sys
################################################################################
class Process:
    def __init__(self, pid, realtime, bytes_s, bytes_e, using_cpu, got_preempted):
        self.pid = pid
        if realtime == True:
            self.realtime = "Realtime"
        else:
            self.realtime = "Common"
        self.bytes_s = bytes_s
        self.bytes_e = bytes_e
        self.using_cpu = using_cpu
        self.got_preempted = got_preempted

################################################################################
def computer_specs():
    #RAM memory
    RAM_memory = int(input("\n\n\tPlease enter amount of RAM memory on simulated computer: "))
    while RAM_memory < 1 or RAM_memory > 4000000000:
        RAM_memory = int(input("\n\n\tRAM memory must be a positive number, up to 4 billion: "))

    #HDD
    num_of_harddisk = int(input("\n\n\tPlease enter number of hard disks on simulated computer: "))
    while num_of_harddisk < 1:
        num_of_harddisk = int(input("\n\n\tAmount of hard disks must be greater than 0: "))

    return RAM_memory, num_of_harddisk;

################################################################################
def preempt(ready_queue):
    for process in ready_queue:
        if process.using_cpu == True and process.realtime == "Common":
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

    #After, check if there are RT processes that were not preempted
    for p in ready_queue:
        if p.using_cpu == False and p.realtime == "Realtime":
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

    #Check if there is a running program, and if so print it first
    for p in ready_queue:
        if p.using_cpu == True:
            print("\t", p.pid, "\t", p.bytes_s, "\t\t", p.bytes_e)

    #Check if there are any preempted processes in the ready_queue
    for p in ready_queue:
        if p.got_preempted == True:
            print("\t", p.pid, "\t", p.bytes_s, "\t\t", p.bytes_e)

    for p in ready_queue:
        if p.using_cpu == False and p.got_preempted == False:
            print("\t", p.pid, "\t", p.bytes_s, "\t\t", p.bytes_e)

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

class Harddisk(list):

    def add_process(self, new_process):
        self.append(new_process)

    def show_queue(self):
        print("\tPID\t  TYPE\t\tSTATUS")
        print("\t--------------------------------")
        for p in self:
            if p.realtime == True:
                p.using_cpu = True
                break
            else:
                self[0].using_cpu = True

        for p in self:
        #Check if there is a serviced procces, and if so print it first
            if p.using_cpu == True:
                print("\t", p.pid, "\t", p.realtime, "\t", "Serviced by HDD")

        for p in self:
            if p.using_cpu == False and p.realtime == "Realtime":
                print("\t", p.pid, "\t", p.realtime, "\t", "Waiting")

        #Print rest of preocesses
        for p in self:
            if p.using_cpu == False and p.realtime == "Common":
                print("\t", p.pid, "\t", p.realtime, "\t", "Waiting")

    def return_process(self, ready_queue):
        for p in self:
            if p.using_cpu == True:
                current_process = p

        for p in ready_queue:
            if p.realtime == "Realtime":
                flag1 = True
            else:
                flag1 = False

        if flag1 == True: #There is a RT process running already
            current_process.using_cpu = False
            ready_queue.append(current_process)
            self.remove(current_process)

        if flag1 == False: #there are no RT processes in RQ
            if current_process.realtime == "Realtime":
                preempt(ready_queue)
                current_process.using_cpu = True
                ready_queue.append(current_process)
                self.remove(current_process)
            elif current_process.realtime == "Common":
                current_process.using_cpu = False
                ready_queue.append(current_process)
                self.remove(current_process)

################################################################################

def main():
    RAM_memory, num_of_harddisk = computer_specs()

    HDD = []
    for drives in range(num_of_harddisk):
        HDD.append(Harddisk())

    ready_queue = []
    pid = 0
    bytes_counter = -1

    while True:

        using_cpu = False
        user_input = str(input(""))
#Add common process
        if user_input.split()[0] == "A":
            pid += 1
            if (not ready_queue):
                using_cpu = True

            new_common_process = Process(pid, False, bytes_counter+1, bytes_counter+int(user_input.split()[1]), using_cpu, False)
            ready_queue.append(new_common_process)
            bytes_counter += int(user_input.split()[1])

#Add realtime process
        elif user_input.split()[0] == "AR":
            flag = False    #flag to check if RQ was empty
            pid += 1
            if not ready_queue:
                using_cpu = True
                new_rt_process = Process(pid, True, bytes_counter+1, bytes_counter + int(user_input.split()[1]), using_cpu, False)
                ready_queue.append(new_rt_process)
                bytes_counter += int(user_input.split()[1])
                flag = True     #ready_queue was empty, added RT process

            if flag == False:   #if RQ was not empty
                for p in ready_queue:
                    if p.realtime == "Realtime":
                        using_cpu = False
                        break
                    else:
                        preempt(ready_queue)   #preempt CPU-using processes, set got_preempted=True
                        using_cpu = True
                new_rt_process = Process(pid, True, bytes_counter+1, bytes_counter + int(user_input.split()[1]), using_cpu, False)
                ready_queue.append(new_rt_process)
                bytes_counter += int(user_input.split()[1])

#show ready queue and running Process
        elif user_input.split()[0] == "S":
            if user_input.split()[1] == "r":
                print_Sr(ready_queue)

#show amount of memory used by each process
            elif user_input.split()[1] == "m":
                print_Sm(ready_queue)
            elif user_input.split()[1] == "i":
                for x in range(num_of_harddisk):
                    print("HDD ", x, ":")
                    HDD[x].show_queue()
                    print("\n\n")

#end time slice of running process
        elif user_input == "Q":
            for p in ready_queue:
                if p.using_cpu == True:
                    current_process = p
                    break
            timeSliceEnded(ready_queue, current_process)

#terminate running Process
        elif user_input == "t":
            for p in ready_queue:
                if p.using_cpu == True:
                    current_process = p
                    break
            terminate_process(ready_queue, current_process)

#move running process to HDD queue
        elif user_input.split()[0] == "d":
            for p in ready_queue:
                if p.using_cpu == True:
                    current_process = p
                    break
            drive_chosen = int(user_input.split()[1])
            HDD[drive_chosen].add_process(current_process)
            chooseNext(ready_queue, current_process)
            ready_queue.remove(current_process)

#HDD finished work for one process
        elif user_input.split()[0] == "D":
            drive_chosen = int(user_input.split()[1])
            HDD[drive_chosen].return_process(ready_queue)



        elif user_input == "quit":
            sys.exit(0)

################################################################################


main()
