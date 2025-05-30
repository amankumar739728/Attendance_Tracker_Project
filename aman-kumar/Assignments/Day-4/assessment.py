#Basics:

#(Question 1.):
print("Hello, world!") #output: Hello, world!

#(Question 2.):

firstname = input("Enter your first name: ").split()
lastname = input("Enter your last name: ").split()
age = int(input("Enter your age: "))

# Concatenate the two lists 
full_name_list = firstname + lastname

# Join the concatenated list into a string
fullname = (" ".join(full_name_list)).title()

print(f"Your name is {fullname} and your age is {age}")


#output: 
# Enter your first name: Aman
# Enter your last name: kumar
# Enter your age: 23
# Your name is Aman Kumar and your age is 23

#(Question 3.):Sum of 2 numbers

num1= int(input("Enter first number: "))
num2= int(input("Enter second number: "))
sum = num1 + num2
print(f"The sum of {num1} and {num2} is {sum}") #output: The sum of 2 and 3 is 5

#(Question 4.): area of circle

import math
radius= float(input("Enter the radius of the circle: "))
area= math.pi * pow(radius, 2)
print(f"The area of the circle with radius {radius} is {area:.2f}") 

#output:
# Enter the radius of the circle: 3
# The area of the circle with radius 3.0 is 28.27


#(Question 5.): swap two numbers(using third variable and tuple unpacking)

#Method 1: using third variable

# num1= int(input("Enter first number: "))
# num2= int(input("Enter second number: "))
num1, num2 =  map(int, input("\nEnter two numbers separated by space: ").strip().split(' '))
print(f"Before swapping values are: num1= {num1} and num2= {num2}")
temp = num1
num1 = num2
num2 = temp
print(f"After swapping using third variable values are: num1= {num1} and num2= {num2}")

#output:
# Enter two numbers separated by space: 2 3
# Before swapping values are: num1= 2 and num2= 3
# After swapping using third variable values are: num1= 3 and num2= 2

#Method 2: using tuple unpacking
num1,num2 = 10,20
print(f"\nBefore swapping using tuple unpacking values are: num1= {num1} and num2= {num2}")
num1, num2 = num2, num1
print(f"After swapping using tuple unpacking values are: num1= {num1} and num2= {num2}")


#output:
# Before swapping using tuple unpacking values are: num1= 10 and num2= 20
# After swapping using tuple unpacking values are: num1= 20 and num2= 10


#Intermediate:
#(Question 6.): check if a number is prime or not

num = int(input("Enter a number: "))
if num > 1:
    for i in range(2, int(num/2)+1):
        if (num % i) == 0:
            print(f"{num} is not a prime number")
            break
    else:
        print(f"{num} is a prime number")
else:
    print(f"{num} is not a prime number")
    
#output:
# Enter a number: 13
# 13 is a prime number

# Enter a number: 10
# 10 is not a prime number


#(Question 7.): print even number from a list
n= int(input("Enter number of elements in the list: "))
list1= []
for i in range(n):
    list1.append(int(input(f"Enter element {i+1}: ")))
print(f"List of even numbers from the list {list1} are: ", end="")
for i in list1:
    if i%2==0:
        print(i, end=" ")
print("\n")

#output:
# Enter number of elements in the list: 5
# Enter element 1: 1
# Enter element 2: 2    
# Enter element 3: 3
# Enter element 4: 4
# Enter element 5: 5    
# List of even numbers from the list [1, 2, 3, 4, 5] are: 2 4

#(Question 8.): Factorial using recursion
def fact(n):
    if n==0 or n==1:
        return 1
    else:
        return n*fact(n-1)
n= int(input("Enter a number: "))
print(f"The factorial of {n} is {fact(n)}")


#output:
# Enter a number: 5
# The factorial of 5 is 120


#(Question 9.): Simple calculator using functions by taking 2 inputs from user and operation choice as input

def add(num1, num2):
    return num1+num2
def sub(num1, num2):
    return num1-num2
def mul(num1, num2):
    return num1*num2
def div(num1, num2):
    return num1/num2
def mod(num1, num2):
    return num1%num2

num1= int(input("Enter first number: "))
num2= int(input("Enter second number: "))
print('''
Enter your choice:
1. Add
2. Subtract
3. Multiply
4. Divide
5. Modulus
''')
choice= int(input("Enter your choice: "))
if choice==1:
    print(f"The sum of {num1} and {num2} is {add(num1,num2)}")
elif choice==2:
    print(f"The difference of {num1} and {num2} is {sub(num1,num2)}")
elif choice==3:
    print(f"The product of {num1} and {num2} is {mul(num1,num2)}")
elif choice==4:
    print(f"The division of {num1} and {num2} is {div(num1,num2)}")
elif choice==5:
    print(f"The modulus of {num1} and {num2} is {mod(num1,num2)}")    
else:
    print("Invalid choice - please try again")
    
    
#output:
# Enter first number: 2
# Enter second number: 3

# Enter your choice:
# 1. Add
# 2. Subtract
# 3. Multiply
# 4. Divide
# 5. Modulus

# Enter your choice: 1
# The sum of 2 and 3 is 5


#(Question 10.): count vowels in a string
def count_vowels(string):
    vowels = "aeiouAEIOU"
    count = 0
    for char in string:
        if char in vowels:
            count += 1
    return count
string = input("Enter a string: ")
print(f"The number of vowels in {string} is {count_vowels(string)}")

#output:
# Enter a string: aman
# The number of vowels in aman is 2


#(Question 11.): check if a string is palindrome or not 

class BankAccount:
    def __init__(self, account_holder, balance=0):
        """Initializing the account with the holder's name and an optional starting balance."""
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        """Deposit a specified amount into the account."""
        if amount > 0:
            self.balance += amount
            print(f"Hi {self.account_holder} ₹{amount} deposited successfully. New Total balance: ₹{self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        """Withdraw a specified amount from the account."""
        if amount > self.balance:
            print("Insufficient balance.")
        elif amount <= 0:
            print("Withdrawal amount must be positive.")
        else:
            self.balance -= amount
            print(f"Hi {self.account_holder} ₹{amount} withdrawn successfully. Remaining balance: ₹{self.balance}")

    def __str__(self):
        """Return a string representation of the account."""
        return f"\nAccount Holder: {self.account_holder}, Balance: ₹{self.balance}"


if __name__ == '__main__':
    account = BankAccount("Aarav", 5000)
    print(account)

    account.deposit(2000)
    account.withdraw(3000)
    account.withdraw(5000)


#output:
# Account Holder: Aarav, Balance: ₹5000
# Hi Aarav ₹2000 deposited successfully. New Total balance: ₹7000
# Hi Aarav ₹3000 withdrawn successfully. Remaining balance: ₹4000
# Insufficient balance.



#Using private and protected members
class BankAccount:
    def __init__(self, account_holder, balance=0):
        """Initializing the account with the holder's name and an optional starting balance."""
        self.__account_holder = account_holder  # Private attribute
        self._balance = balance  # Protected attribute

    def deposit(self, amount):
        """Deposit a specified amount into the account."""
        if amount > 0:
            self._balance += amount
            print(f"Hi {self.__account_holder} ₹{amount} deposited successfully. New Total balance: ₹{self._balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        """Withdraw a specified amount from the account."""
        if amount > self._balance:
            print("Insufficient balance.")
        elif amount <= 0:
            print("Withdrawal amount must be positive.")
        else:
            self._balance -= amount
            print(f"Hi {self.__account_holder} ₹{amount} withdrawn successfully. Remaining balance: ₹{self._balance}")

    def __str__(self):
        """Return a string representation of the account."""
        return f"\nAccount Holder: {self.__account_holder}, Balance: ₹{self._balance}"
# Example usage:
account = BankAccount("Aarav", 5000)
print(account)

account.deposit(2000)
account.withdraw(3000)
account.withdraw(5000)

#output:
# Account Holder: Aarav, Balance: ₹5000
# Hi Aarav ₹2000 deposited successfully. New Total balance: ₹7000
# Hi Aarav ₹3000 withdrawn successfully. Remaining balance: ₹4000
# Insufficient balance.



#(Question 12.): define a decorator function and call its method name and perform sample function call

# Decorator function
def decorator_function(func):
    def wrapper(*args, **kwargs):
        print(f"\nCalling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Sample function with decorator applied
@decorator_function
def greet(name):
    print(f"Hello, {name}!")

# Example usage
greet("Alice")


#output:

# Calling function: greet
# Hello, Alice!


#(Question 13.): read and write to a file (using pathlib)
#use open() method to read and write to a file and print the content of the file
#handle exceptions using try and except if file not found

    
from pathlib import Path

# Define the file path
file_path = Path("example.txt")

if not file_path.exists():
    print(f"File '{file_path}' does not exist and will be created.")
else:
    print(f"File '{file_path}' already exists and will be overwritten.")

# Write to the file (creates if it doesn't exist)
try:
    file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    with file_path.open("w", encoding="utf-8") as file:
        file.write("Hello, this is a test file.\n")
        file.write("This is the second line.\n")
    print(f"Data written to {file_path.resolve()}")
except Exception as e:
    print(f"Error writing file: {e}")

# Read from the file
try:
    with file_path.open("r", encoding="utf-8") as file:
        content = file.read()
        print(f"Content of {file_path}:\n{content}")
except Exception as e:
    print(f"Error reading file: {e}")


#output:
# File 'example.txt' does not exist and will be created.
# Data written to C:\Users\AmanKumar\OneDrive - GyanSys Inc\Desktop\gs-upskill-python-2025\workarea\aman-kumar\Assignments\Day-4\example.txt
# Content of example.txt:
# Hello, this is a test file.
# This is the second line.


#(Question 14.): weather data using API
#use requests module to get the data from OpenWeatherMap API
#parse the JSON data and print the city name, temperature, humidity, and weather description
#handle exceptions using try and except if API key is invalid or city not found
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
# Load environment variables
API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

try:
    # Make a request to the OpenWeatherMap API
    response = requests.get(BASE_URL, params={"q": CITY, "appid": API_KEY, "units": "metric"})
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the JSON data
    weather_data = response.json()

    # Extract relevant information
    city_name = weather_data["name"]
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    weather_description = weather_data["weather"][0]["description"]

    # Print the weather information
    print(f"City: {city_name}")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Weather Description: {weather_description}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching weather data: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    
    
    