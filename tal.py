# Tal Bachar
# CSCI 340
# Home Project
# Prof. Pavel Shostak

class Process:

    def __init__(self, pid, realtime, bytes):
        self.pid = pid
        self.realtime = realtime
        self.bytes = bytes

    def pcb(self):
        print("\t", self.pid, "\t ", self.realtime, "\t", self.bytes)


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

    process_list = []
    pid = 0

    while True:

        user_input = str(input(""))

        if user_input.split()[0] == "A":
            pid += 1
            process_list.append(Process(pid, False, user_input.split()[1]))
        elif user_input.split()[0] == "AR":
            pid += 1
            process_list.append(Process(pid, True, user_input.split()[1]))
        elif user_input.split()[0] == "S":
            if user_input.split()[1] == "r":
                print("\tPID \t  TYPE \t STATUS")
                for p in process_list:
                    p.pcb()





main()
