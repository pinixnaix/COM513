"""
activity that open a file and asks the user for more devices to be added to the file
"""

def menu():
    """ Function to display a menu"""
    print("-"*20+" DEVICES "+"-"*20)

    print("\n[1] - Read the devices from the text file"
          "\n[2] - Add devices to the text file"
          "\n[3] - Exit")
        
    try:
        option = int(input("Please choose an option: "))
    except ValueError:
        option = int(input("Error!!! Please enter a valid option: "))
    except TypeError:
        option = int(input("Error!!! Please enter a valid option: "))
    return option


def read_file(path):
    print(path)
    return

def write_file(path):
    return


def run():
    """Main function"""
    while True:
        option = menu()
        if option == 1:
            read_file("devices.txt")
        elif option == 2:
            write_file("devices.txt")
        elif option ==3:
            break
    
if __name__ == '__main__':
    run()
