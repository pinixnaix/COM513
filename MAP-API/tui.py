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
    sleep(5)


def menu(variant):
    """Function to display a menu"""

    if variant is None or variant == 0:
        choices = [1, 2, 3, 4]
        print("[1] Enter the Directions")
        print("[2] Visualise Data")
        print("[3] Export Data")
        print("[4] Exit")
        option = int(input())
        if option in choices:
            return option
        else:
            print("Wrong Option!!!!!")
            return None

    return
