"""
Text User interface application
"""
from time import sleep
import os


def welcome():
    os.system("clear")
    print("="*75+"\n\n\n")
    print("\t\t\t\tWELCOME\n\n\n")
    print("\tThis application will retrieve JSON data from the MapQuest API")
    print("="*75)
    sleep(5)
