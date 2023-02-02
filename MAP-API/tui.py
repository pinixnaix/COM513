"""
Text User interface application
"""
from time import sleep
import os


def welcome():
    """Function to display a welcome message"""
    os.system("clear")
    print("="*75+"\n\n\n")
    print("\t\t\t\tWELCOME\n\n\n")
    print("\tThis application will retrieve JSON data from the MapQuest API")
    print("="*75)
    sleep(3)


def exit():
    """Function to display a exit message"""
    os.system("clear")
    print("="*75+"\n\n\n")
    print("\t\t\t\tExit\n\n\n")
    print("\t\t\tThank you for using this API")
    print("="*75)
    sleep(3)


def menu(variant):
    """Function to display a menu"""

    if variant is None or variant == 0:
        os.system("clear")
        choices = [1, 2, 3, 4]
        print("="*75+"\n\n")
        print("\t\t\t\tMain Menu\n\n")

        print("[1] Enter the Directions")
        print("[2] Visualise the result ")
        print("[3] Options for the search ")
        print("[4] Exit")
        option = int(input())
        if option in choices:
            return option
        else:
            print("Wrong Option!!!!!")
            return None

    elif variant == 1:
        os.system("clear")
        print("="*75+"\n\n")
        print("\t\tEnter the Directions\n")
        location = str(input("\nEnter the starting location: "))
        destination = str(input("\nEnter the destination: "))

        return (location, destination)

    elif variant == 3:

        os.system("clear")
        choices = [1, 2, 3, 4]
        print("="*75+"\n\n")
        print("\t\tChange the options for the navigation\n")
        print("[1] Change starting location")
        print("[2] Change destination")
        print("[3] Change API url")
        print("[4] Change key")

        option = int(input())

        if option in choices:
            return option
        else:
            print("Wrong Option!!!!!")
            return None

    elif variant == 4:
        return str(input("\nEnter new starting Location: "))
    elif variant == 5:
        return str(input("\nEnter new destination: "))
    elif variant == 6:
        return str(input("\nEnter new API url: "))
    elif variant == 7:
        return str(input("\nEnter new key: "))
    elif variant == 8:
        os.system("clear")
        choices = [1, 2]
        print("="*75+"\n\n")
        print("Please choose one of the options to display the data for the navigation\n")
        print("[1] Display in imperial")
        print("[2] Display in metric")

        option = int(input())

        if option in choices:
            return option
        else:
            print("Wrong Option!!!!!")
            return None 

def display(data, option, loc, dest, url):
    """ Function to display the data"""
    os.system("clear")
    print("="*75+"\n\n")
    print("URL: "+url)
    print("\nStarting Location: "+loc)
    print("Destination: "+dest)

    if option == 1:
        print("in MPG")
    else:
        print("in KM")
    try:
        input("Press enter to continue ")
    except SyntaxError:
        pass
