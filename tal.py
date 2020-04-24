# Tal Bachar
# CSCI 340
# Home Project
# Prof. Pavel Shostak

class Process:
    def __init__(self, pid, realtime, bytes, using_cpu):
        self.pid = pid
        if realtime == True:
            self.realtime = "REALTIME"
        else:
            self.realtime = "COMMON"
        self.bytes = bytes
        self.using_cpu = using_cpu

    def pcb(self):
       print("\t", self.pid, "\t", self.realtime, "\t", end=" ")
       if self.using_cpu:
           print("RUNNING")
       else:
           print("WAITING")



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

##################################################################
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

            new_common_process = Process(pid, False, user_input.split()[1], using_cpu)
            ready_queue.append(new_common_process)

        #Add realtime process
        elif user_input.split()[0] == "AR":
            pid += 1
            using_cpu = True
            new_rt_process = Process(pid, True, user_input.split()[1], using_cpu)
            ready_queue.append(new_rt_process)


        elif user_input.split()[0] == "S":
            if user_input.split()[1] == "r":
                print("\tPID\t  TYPE\t\tSTATUS")
                print("\t-------------------------------")

                for p in ready_queue:
                    p.pcb()





main()
