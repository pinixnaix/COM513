"""
personal info input
"""

def run():

    first_name=str(input("What is your first name? "))
    last_name=str(input("What is your last name? "))
    location=str(input("What is your location? "))
    age=str(input("What is your age? "))
    print(f"Hi {first_name} {last_name}! Your location is {location} and you are {age} years old.")
    
if __name__ == '__main__':
    run()