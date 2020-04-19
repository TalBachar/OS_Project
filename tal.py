# Tal Bachar
# CSCI 340
# Home Project
# Prof. Pavel Shostak

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

def user_action():
    action = str(input(""))
    print(action.split()[0])




def main():
    RAM_memory, num_of_harddisk = computer_specs()

    user_action()





main()
