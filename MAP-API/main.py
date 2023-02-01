"""
Application that retrieves JSON data from the MapQuest Directions API,
parses the data, and formats it for output to the user
"""
import urllib.parse
import requests
import tui, process


def run():

    tui.welcome()


if __name__ == "__main__":
    run()
