"""
Application that retrieves JSON data from the MapQuest Directions API,
parses the data, and formats it for output to the user
"""

from time import sleep
import tui, process

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "2I7zK0gJWAdbdb1vlRAawWHYziJtCztn"
location = ""
destination = ""


def run():
    """ main function to run the JSON applicaiton"""
    global location, key, destination, main_api
    
    tui.welcome()
    while True:
        option = tui.menu(0)

        if option == 1:
            directions = tui.menu(1)
            location = directions[0]
            destination = directions[1]

        elif option == 2:
            new_url = process.url(main_api, key, location, destination)
            data = process.retrieve_json(new_url)
            print(data)
            sleep(5)
        elif option == 3:
            choice = tui.menu(3)
            if choice == 1:
                location = tui.menu(4)
            elif choice == 2:
                destination = tui.menu(5)
            elif choice == 3:
                main_api = tui.menu(6)
            elif choice == 4:
                key = tui.menu(7)
        elif option == 4:
            break


if __name__ == "__main__":
    run()
