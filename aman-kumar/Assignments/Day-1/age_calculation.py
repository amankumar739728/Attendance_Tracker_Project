#Calculate the age of a person after 5 years and print it with f-string

def display():
    try:
        name = input("Enter your name: ")
        age = int(input("Enter the age: "))
        print(f"Hi {name} your age after 5 years will be {age+5}")
    except ValueError:
        print("Invalid input. Please enter a number.")
    finally:
        print("Program Executed Successfully!")
display()


#OR

import re
def calculate_future_age(current_age, years_ahead=5):
    return current_age + years_ahead

def get_valid_name():
    while True:
        name = input("Enter your name: ").strip()
        if not name:  # This checks if the name is empty after stripping
            print("Name cannot be empty. Please enter a valid name.")
            continue
        # Replace multiple spaces with a single space
        name = re.sub(r'\s+', ' ', name)
        return name

def get_valid_age():
    while True:
        try:
            age = int(input("Enter your age: "))
            if age < 0:
                print("Age cannot be negative. Please try again.")
                continue
            return age
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_age_info():
    try:
        name = get_valid_name()
        age = get_valid_age()
        future_age = calculate_future_age(age)
        print(f"Hi {name}, your age after 5 years will be {future_age}")
    finally:
        print("Program Executed Successfully!")

if __name__ == "__main__":
    display_age_info()
    
    
    
#Question-2:
# Write a reusable function to: Take a list of numbers andReturn the count of even and odd numbers

def even_odd_count(numbers):
    even_count,odd_count = 0,0
    for num in numbers:
        if num % 2 == 0:
            even_count += 1
        else:
            odd_count += 1

    return even_count, odd_count

numbers = [1, 2, 3, 4, 5, 6]
even_count, odd_count = even_odd_count(numbers)
print(f"Even count: {even_count} \nOdd count: {odd_count}")


#Sample-output:
#Even count: 3
#Odd count: 3