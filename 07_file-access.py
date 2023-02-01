"""
activity that open a file and asks the user for more devices to be added to the file
"""
import os


def menu():
    """ Function to display a menu"""
    os.system("clear")
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
    os.system("clear")
    with open(path) as file:
        data = file.read()
        print(data)
    try:
        input("Press enter to continue ")
    except SyntaxError:
        pass
    

def write_file(path):
    """Function to add devices to the text file"""
    os.system("clear")
    with open(path, "a") as file:
        while True:
            new_device = str(input("Enter device name: "))
            if new_device == "exit":
                print("\n"+"-"*50+"\n"+" "*17+"All DONE!!!\n"+"-"*50)
                break
            else:    
                file.write(new_device+"\n")


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
