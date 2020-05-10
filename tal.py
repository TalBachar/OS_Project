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
class MemoryHoles(list):


# when process is terminated, will create a list of start of memory hole and end of memory hole
    def insert_hole(self, terminated_process):
        bytes_list = [terminated_process.bytes_s, terminated_process.bytes_e]
        self.append(bytes_list)
        self.organize_list()

# will check in all memory holes if the space needed fits in one of the holes.
# if it fits, new process will be assinged to fill hole, and the hole will shrink accordingly.
# if it doesn't fit, will return sentinel (-1)
    def check_available_holes(self, needed_space):
        sentinel = -1
        if not self:
            return sentinel
        for holes in self:
            if ((holes[1] - holes[0]) + 1) >= needed_space:
                start_mem = int(holes[0])
                holes[0] += needed_space
                self.organize_list()
                return start_mem
        return sentinel



    def organize_list(self):
        self.sort(key=lambda x: x[0])
        for i in self:
            if i[0] >= i[1]:
                self.remove(i)

        for thisHole,nextHole in zip(self, self[1:]):
            start = thisHole[0]
            end = nextHole[1]

            if thisHole[1] + 1 == nextHole[0]:
                self.remove(thisHole)
                self.remove(nextHole)
                new_hole_range = [start, end]
                self.append(new_hole_range)
                self.sort(key=lambda x: x[0])



    def print_list(self):
        print(self)

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

        for p in ready_queue:   #check if there is a RT process in the RQ
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

################################################################################
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
        if p.got_preempted == True and p.realtime == "Realtime" and p != current_process:
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

    HDD = []
    for drives in range(num_of_harddisk):
        HDD.append(Harddisk())

    mem_holes = MemoryHoles()
    ready_queue = []
    pid = 0
    bytes_counter = -1

    while True:

        using_cpu = False
        user_input = str(input(""))
#Add common process
        if user_input.split()[0] == "A":
            if (bytes_counter + int(user_input.split()[1])) > RAM_memory:
                print("Memory used exceeds RAM memory available!")

            else:
                available_hole = 0
                pid += 1
                if (not ready_queue):
                    using_cpu = True

                available_hole = mem_holes.check_available_holes(int(user_input.split()[1]))
                if available_hole >= 0:
                    print("Creating process in hole, mem_start at:", available_hole)
                    new_common_process = Process(pid, False, available_hole,
                                         (available_hole+int(user_input.split()[1])-1), using_cpu, False)
                else:
                    new_common_process = Process(pid, False, (bytes_counter+1),
                                     (bytes_counter+int(user_input.split()[1])), using_cpu, False)
                    bytes_counter += int(user_input.split()[1])

                ready_queue.append(new_common_process)

#Add realtime process
        elif user_input.split()[0] == "AR":
            if (bytes_counter + int(user_input.split()[1])) > RAM_memory:
                print("Memory used exceeds RAM memory available!")

            else:
                available_hole = 0
                flag = False    #flag to check if RQ was empty
                pid += 1
                if not ready_queue:
                    available_hole = mem_holes.check_available_holes(int(user_input.split()[1]))
                    using_cpu = True
                    if available_hole >= 0:
                        print("Creating process in hole, mem_start at:", available_hole)
                        new_rt_process = Process(pid, True, available_hole,
                                        (available_hole + int(user_input.split()[1]) -1), using_cpu, False)
                    else:
                        new_rt_process = Process(pid, True, (bytes_counter+1),
                                         (bytes_counter + int(user_input.split()[1])), using_cpu, False)
                        bytes_counter += int(user_input.split()[1])

                    ready_queue.append(new_rt_process)
                    flag = True     #ready_queue was empty, added RT process

                if flag == False:   #if RQ was not empty
                    available_hole = mem_holes.check_available_holes(int(user_input.split()[1]))

                    for p in ready_queue:
                        if p.realtime == "Realtime":
                            using_cpu = False
                            break
                        else:
                            preempt(ready_queue)   #preempt CPU-using processes, set got_preempted=True
                            using_cpu = True
                    if available_hole >= 0:
                        print("Creating process in hole, mem_start at:", available_hole)
                        new_rt_process = Process(pid, True, available_hole,
                                        (available_hole + int(user_input.split()[1]) -1), using_cpu, False)
                    else:
                        new_rt_process = Process(pid, True, (bytes_counter+1),
                                         (bytes_counter + int(user_input.split()[1])), using_cpu, False)
                        bytes_counter += int(user_input.split()[1])
                    ready_queue.append(new_rt_process)

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
            if ready_queue:
                mem_holes.insert_hole(current_process)
                terminate_process(ready_queue, current_process)
            else:
                print ("Ready queue is empty")


#move running process to HDD queue
        elif user_input.split()[0] == "d":
            for p in ready_queue:
                if p.using_cpu == True:
                    current_process = p
                    break
            drive_chosen = int(user_input.split()[1])

            if drive_chosen > num_of_harddisk:
                print ("HDD", drive_chosen, "does not exist")
            elif ready_queue:
                HDD[drive_chosen].add_process(current_process)
                chooseNext(ready_queue, current_process)
                ready_queue.remove(current_process)
            else:
                print ("Ready queue is empty")

#HDD finished work for one process
        elif user_input.split()[0] == "D":
            drive_chosen = int(user_input.split()[1])
            if drive_chosen > num_of_harddisk:
                print ("HDD", drive_chosen, "does not exist")
            else:
                if HDD[drive_chosen]:
                    HDD[drive_chosen].return_process(ready_queue)
                else:
                    print ("HDD", drive_chosen,"queue is empty")

#quit option
        elif user_input == "quit":
            sys.exit(0)

#invalid
        else:
            print(user_input, "is not a valid action!\n")

################################################################################


main()
