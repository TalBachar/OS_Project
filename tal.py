# Tal Bachar
# CSCI 340
# Home Project
# Prof. Pavel Shostak

class Process:

    def __init__(self, realtime, bytes):
        self.realtime = realtime
        self.bytes = bytes

    def pcb(self):
        print(self.realtime)
        print(self.bytes)

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

'''
def user_action():
    action = str(input(""))

    if action.split()[0] == "A":
        Process(False, action.split()[1])
    elif action.split()[0] == "AR":
        Process(True, action.split()[1])
'''
##################################################################
def main():
    RAM_memory, num_of_harddisk = computer_specs()

    process_list = []

    while True:
        user_input = str(input(""))

        if user_input.split()[0] == "A":
            process_list.append(Process(False, user_input.split()[1]))
        elif user_input.split()[0] == "AR":
            process_list.append(Process(True, user_input.split()[1]))
        break



    for obj in process_list:
        obj.pcb()


main()
'''
            # Python3 code here for creating class
        class geeks:
        	def __init__(self, x, y):
        		self.x = x
        		self.y = y

        	def Sum(self):
        		print( self.x + self.y )

        # creating list
        list = []

        # appending instances to list
        list.append( geeks(2, 3) )
        list.append( geeks(12, 13) )
        list.append( geeks(22, 33) )

        for obj in list:
        	# calling method
        	obj.Sum()

        # We can also access instances method
        # as list[0].Sum, list[1].Sum and so on.
'''
