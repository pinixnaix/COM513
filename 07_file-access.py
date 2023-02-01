"""
activity that open a file and asks the user for more devices to be added to the file
"""

def menu():
    """ Function to display a menu"""
    print("-"*50+"\n"+" "*17+"NETWORK DEVICES \n"+"-"*50)

    print("\n[1] - Read the devices from the text file"
          "\n[2] - Add devices to the text file"
          "\n[3] - Exit")
        
    try:
        option = int(input("\nPlease choose an option: "))
    except ValueError:
        option = int(input("Error!!! Please enter a valid option: "))
    except TypeError:
        option = int(input("Error!!! Please enter a valid option: "))
    return option


def read_file(path):
    """Function to read and print the devices text file"""
    with open(path) as file:
        data = file.read()
        print(data)

def write_file(path):
    """Function to add devices to the text file"""
    with open(path) as file:
        data = file.read()
        print(data)


def run():
    """Main function"""
    while True:
        option = menu()
        if option == 1:
            read_file("devices.txt")
        elif option == 2:
            write_file("/workspaces/COM513/devices.txt")
        elif option ==3:
            print("\n"+"-"*50+"\n"+" "*17+"THANK YOU!!!\n"+"-"*50)
            break

if __name__ == '__main__':
    run()
