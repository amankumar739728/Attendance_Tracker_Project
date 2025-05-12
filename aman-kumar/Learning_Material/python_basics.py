##############################################################
#Topic: Python Basics
#Author: Aman Kumar
#Date: 6th May,2025
#Role: Backend Developer
#Company: GyanSys Inc.
#Email: aman.kumar@gyansys.com
##############################################################


# Python Basic Syntax:

""" Python is a high-level, interpreted programming language known for its readability and simplicity. 
It's widely used in data science, web development, automation, and more. """

# 1. Comments
# 2. Indentation and Spacing
# 3. Variables
# 4. Data Types
# 5. Operators
# 6. Control Flow
# 7. Functions
# 8. Exception Handling
# 9. File Operations
# 10. Modules and Imports
# 11. Regular Expressions
# 12. Working with Dates and Times





# 1. Comments
# This is a single line comment
print("Hello, World!")  # This is an inline comment

# This is a multiline comment

print(f"""
This is a multiline comment,
and this is related to python.
""")


#2. Indentation and Spacing

# Indentation
# Indentation is used to define a block of code in Python.
# It is done using spaces or tabs.

n1,n2=10,20
num=int(input("Enter a number: ")) #user will enter 15
if num>=n1 and num<=n2:
    print("In range")
else:
    print("Out of Range")


#3. Variables
name = "John" #String variables can be declared either by using single or double quotes
age = 25 #Variable names are case-sensitive (age and Age are different variables)
height = 5.9
is_student = True


print(name)
print(age)
print(height)
print(is_student)
print(f"age: {age} (type: {type(age)})")

#Note: Rules for naming variables
# 1. Variable names must start with a letter or underscore (_)
# 2. Variable names can only contain alpha-numeric characters and underscores
# 3. Variable names are case-sensitive
# 4. Variable names should be descriptive and meaningful
# 5. Variable names should not be a reserved keyword in Python(can not be if,else etc)
# 6. Variable names should not start with a number
# 7. Variable names should not contain special characters like !, @, #, $, %, ^, &, *, (, ), _, +, =, <, >, ?, /, \, |, ~
# 8. Variable names should not be too long, it should be short and meaningful



#4. Data Types

# 1. String
# 2. Integer
# 3. Float
# 4. Boolean
# 5. List
# 6. Tuple
# 7. Set
# 8. Dictionary



# String
txt = "We are the so-called \"Vikings\" from the north."
name = "Alice"
a = "Hello, World!"


#--> String Operations
print(name[0]) #Accessing a character in a string (output: A)
print(name[-1]) #Accessing the last character in a string(output: e)
print(name[1:4]) #Accessing a substring in a string (output: lic)
print(a.upper()) #Converting a string to uppercase (output: HELLO, WORLD!)
print(a.lower()) #Converting a string to lowercase (output: hello, world!)
print(a.capitalize()) #Converting the first character of a string to uppercase (output: Hello, world!)
print(a.title()) #Converting the first character of each word in a string to uppercase (output: Hello, World!)
print(a.split(",")) #Splitting a string into a list of substrings(output: ['Hello', ' World!'])
print(a.replace("World", "Aman")) #Replacing a substring in a string (output: Hello, Aman!)
print(a.strip()) #Removing leading and trailing spaces from a string (output: Hello, World!)
print(a.startswith("Hello")) #Checking if a string starts with a certain substring (output: True)
print(a.endswith("World!")) #Checking if a string ends with a certain substring (output:
print(a.find("World")) #Finding the index of a substring in a string (output: 7)
print(a.count("o")) #Counting the number of occurrences of a substring in a string (output: 3)
print(a.center(50,"*")) #Centering a string in a certain width (output: ***************Hello, World!***************)
print(txt) #Escaping special characters in a string(output: We are the so-called "Vikings" from the north.)


# Integer
x = 10

# Float
y = 15.2

# Boolean
is_valid = True

# List
fruits = ["apple", "banana", "cherry"]

# Tuple
coordinates = (10.0, 20.0)

# Set
unique_numbers = {1, 2, 3, 4, 5}

# Dictionary
person = {"name": "Alice", "age": 25}



#--> Data Types
print(type(name)) #output: <class 'str'>
print(type(x)) #output: <class 'int'>
print(type(y)) #output: <class 'float'>
print(type(is_valid)) #output: <class 'bool'>
print(type(fruits)) #output: <class 'list'>
print(type(coordinates)) #output: <class 'tuple'>
print(type(unique_numbers)) #output: <class 'set'>
print(type(person)) #output: <class 'dict'>


#--> Type Conversion
x = 10
y = 15.2
print(type(x)) #output: <class 'int'>
print(type(y)) #output: <class 'float'>
print(float(x)) #output: 10.0
print(int(y)) #output: 15
print(str(x) + " " + str(y)) #output: 10 15.2
print(x + y) #output: 25.2
print(x + int(y)) #output: 25
print(str(x) + str(y)) #output: 1015.2


########NOTE################################################

#List: Ordered,Mutable(changable), Allow-duplicates
#Tuple: Ordered,Immutable(unchangable),Allow-duplicates
#Set: Unordered,Immutable(unchangable),No-duplicates allowed
#Dictionary: Ordered,Mutable,No-duplicates allowed,Key-value pairs

#List:
list1 = [1,2,3,4,5]
print(list1[0]) #output: 1
print(list1[-1]) #output: 5
print(list1[1:4]) #output: [2, 3, 4]
#Operations:
#append() - Add an element to the end of the list
#extend() - Add multiple elements to the end of the list
#insert() - Add an element at a specific index in the list
#remove() - Remove an element from the list
#pop() - Remove an element at a specific index in the list
#clear() - Remove all elements from the list
#copy() - Create a copy of the list
#count() - Count the number of occurrences of an element in the list
#index() - Find the index of an element in the list
#reverse() - Reverse the order of the elements in the list
#sort() - Sort the elements in the list in ascending order
#reverse() - Reverse the order of the elements in the list
#sort() - Sort the elements in the list in ascending order

#Example:
list2 = [1,2,3,4,5]
print(list2) #output: [1, 2, 3, 4, 5]
list2.append(6) #output: [1, 2, 3, 4, 5, 6]
list2.extend([7,8,9]) #output: [1, 2, 3, 4, 5, 6, 7, 8, 9]
list2.insert(2,10) #output: [1, 2, 10, 3, 4, 5, 6, 7, 8, 9]
list2.remove(4) #output: [1, 2, 10, 3, 5, 6, 7, 8, 9]
list2.pop(2) #output: [1, 2, 3, 5, 6, 7, 8, 9]
list2.copy() #output: [1, 2, 3, 5, 6, 7, 8, 9]
list2.count(3) #output: 1
list2.index(5) #output: 3
list2.reverse() #output: [9, 8, 7, 6, 5, 3, 2, 1]
list2.sort() #output: [1, 2, 3, 5, 6, 7, 8, 9]
list2.sort(reverse=True) #output: [9, 8, 7, 6, 5, 3, 2, 1]
list3=[6,1,2,3,4,5]
l2=sorted(list3)
print(l2) #output: [1, 2, 3, 4, 5, 6]
print(list1.clear()) #output: None ([]--> list1 is now empty)

#List Comprehension:(List comprehension is a compact way to create lists in Python.)

#Example:
squared_numbers = [x**2 for x in range(5)]
print(squared_numbers) #output: [0, 1, 4, 9, 16]

#Join 2 lists:
list1 = [1, 2, 3]
list2 = [4, 5, 6]
print(list1 + list2) #output: [1, 2, 3, 4, 5, 6]


#copy a list
list4 = [1,2,3,4,5]
list_copy = list4.copy()
print(list_copy) #output: [1, 2, 3, 4, 5]

#or:
thislist = [1,2,3,4,5]
mylist = list(thislist)
print(mylist) #output: [1, 2, 3, 4, 5]



#Tuple:(can be changable after type casting it to list)

thistuple = ("apple",)
print(type(thistuple)) #output: <class 'tuple'>

#NOT a tuple
thistuple = ("apple")
print(type(thistuple))  #output: <class 'str'>


tuple = (1,2,3,4,5)
print(tuple) #output: (1, 2, 3, 4, 5)
print(tuple[0]) #output: 1
print(tuple[-1]) #output: 5
print(tuple.count(3)) #output: 1
print(tuple.index(3)) #output: 2
print(tuple + (6,7,8)) #output: (1, 2, 3, 4, 5, 6, 7, 8)
print(tuple * 2) #output: (1, 2, 3, 4, 5, 1, 2, 3, 4, 5)


#join 2 tuples:
tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)

tuple3 = tuple1 + tuple2
print(tuple3) #output: ('a', 'b', 'c', 1, 2, 3)


#set:
set1 = {1,2,3,4,5}
print(set1) #output: {1, 2, 3, 4, 5}
print(type(set1)) #output: <class 'set'>
set2 = set([1,2,3,4,5])
print(set2) #output: {1, 2, 3, 4, 5}
set3 = set((1,2,3,4,5))
print(set3) #output: {1, 2, 3, 4, 5}
set4 = set({1,2,3,4,5})
print(set4) #output: {1, 2, 3, 4, 5}
set5 = set("Hello")
print(set5) #output: {'H', 'o', 'l', 'e'}
#set operations:
set1 = {1,2,3,4,5}
set2 = {4,5,6,7,8}
print(set1.union(set2)) #output: {1, 2, 3, 4, 5, 6, 7, 8}
print(set1.intersection(set2)) #output: {4, 5}
print(set1.difference(set2)) #output: {1, 2, 3}
print(set1.symmetric_difference(set2)) #output: {1, 2, 3, 6, 7, 8}

#dictionary:
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}
print(person) #output: {'name': 'Alice', 'age': 25, 'city': 'New York'}
print(person["name"]) #output: Alice
person["age"] = 26
print(person) #output: {'name': 'Alice', 'age': 26, 'city': 'New York'}
person["country"] = "USA"
print(person) #output: {'name': 'Alice', 'age': 26, 'city': 'New York', 'country': 'USA'}
del person["country"]
print(person) #output: {'name': 'Alice', 'age': 26, 'city': 'New York'}
person.clear()
print(person) #output: {}
#dictionary operations:
dict1 = {"a": 1, "b": 2, "c": 3}
dict2 = {"d": 4, "e": 5, "f": 6}
dict3 = dict1.copy()
print(dict3) #output: {'a': 1, 'b': 2, 'c': 3}
dict1.update(dict2)
print(dict1) #output: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
print(dict1.keys()) #output: dict_keys(['a', 'b', 'c', 'd', 'e', 'f'])
print(dict1.values()) #output: dict_values([1, 2, 3, 4, 5, 6])
print(dict1.items()) #output: dict_items([('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5), ('f', 6)])

#loop dictionary:
dict1 = {"a": 1, "b": 2, "c": 3}
for key,value in dict1.items():
    print(f"({key},{value})") #output: ('a',1) ('b',2) ('c',3)
    
keys_list = list(dict1.keys())
print(keys_list)  #output: ['a', 'b', 'c']
values_list = list(dict1.values())
print(values_list)  #output: [1, 2, 3]




#5. Operators

# 1. Arithmetic Operators
# 2. Assignment Operators
# 3. Comparison Operators
# 4. Logical Operators
# 5. Membership Operators
# 6. Identity Operators
# 7. Bitwise Operators
# 8. Augmented Assignment Operators
# 9. Conditional Operators

# Arithmetic Operators
x = 10
y = 5
print(x + y)  # 15
print(x - y)  # 5
print(x * y)  # 50
print(x / y)  # 2.0
print(x // y)  # 2
print(x % y)  # 0
print(x ** y)  # 1000

# String operations
greeting = "Hello"
name = "Alice"
print(greeting + ", " + name)  # Concatenation (output: Hello, Alice)
print(greeting * 3)  # Repetition (output: HelloHelloHello)

a = "Hello, World!"
print(len(a)) #output: 13

b = "Hello, World!" #string slicing
print(b[-5:-2])#output: orl

# Assignment Operators
x = 10
print(x)  # 10
x += 5
print(x)  # 15
x -= 5
print(x)  # 10
x *= 5
print(x)  # 50
x /= 5
print(x)  # 10.0
x //= 5
print(x)  # 2.0
x %= 5
print(x)  # 0.0
x **= 5
print(x)  # 1.0

# Comparison Operators
x = 10
y = 5
print(x == y)  # False
print(x != y)  # True
print(x > y)  # True
print(x < y)  # False
print(x >= y)  # True
print(x <= y)  # False

# Logical Operators
x = True
y = False
print(x and y)  # False 
print(x or y)  # True
print(not x)  # False

# Membership Operators
fruits = ["apple", "banana", "cherry"]
print("apple" in fruits)  # True
print("grape" not in fruits)  # True

# Identity Operators
x = 10
y = 10
print(x is y)  # True
print(x is not y)  # False

# Bitwise Operators
x = 10
y = 5
print(x & y)  # 0
print(x | y)  # 15
print(x ^ y)  # 15
print(~x)  # -11
print(x << 2)  # 40
print(x >> 2)  # 2

# Augmented Assignment Operators
x = 10
x += 5
print(x)  # 15
x -= 5
print(x)  # 10
x *= 5
print(x)  # 50
x /= 5
print(x)  # 10.0
x //= 5
print(x)  # 2.0
x %= 5
print(x)  # 0.0
x **= 5
print(x)  # 1.0

# Conditional Operators
x = 10
y = 5
print(x if x > y else y)  # 10


#6. Control Flow


# 1. If-Else
# 2. For Loop
# 3. While Loop
# 4. Break
# 5. Continue
# 6. Pass
# 7. Return
# 8. Nested Loops
# 9. Ternary Operator
# 10. Lambda Functions
# 11. Generator Expressions
# 12. List Comprehension
# 13. Dictionary Comprehension
# 14. Set Comprehension
# 15. Yield
# 16. Nonlocal
# 17. Global

# 1. If-Else
x = 10
if x > 5:
    print("x is greater than 5")
else:
    print("x is less than or equal to 5") #output: x is less than or equal to 5



#example2:

x = 15

if x > 20:
    print("x is greater than 20")
elif x > 10:
    print("x is greater than 10 but not greater than 20")
else:
    print("x is not greater than 10") #output: x is greater than 10 but not greater than 20



# 2. For Loop:
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)   #output: apple banana cherry
    
#example 2:
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(index, fruit) #output: 0 apple 1 banana 2 cherry
    
    
    


# 3. While Loop:
count = 0
while count < 5:
    print(count, end=" ")
    count += 1
print() #for keeping a new line(next output will be displayed in a new line) #output: 0 1 2 3 4

# 4. Break:
for i in range(10):
    if i == 5:
        break
    print(i) #output: 0 1 2 3 4

# 5. Continue:
for i in range(10):
    if i == 5:
        continue
    print(i) #output: 0 1 2 3 4 6 7 8 9

# 6. Pass:
for i in range(10):
    if i == 5:
        pass
    print(i) #output: 0 1 2 3 4 5 6 7 8 9

# 7. Return:
def add(x, y):
    return x + y
print(add(1, 2)) #output: 3

# 8. Nested Loops:
for i in range(3):
    for j in range(3):
        print(i, j) #output: 0 0 0 1 1 1 2 2 2

# 9. Ternary Operator:
x = 10
print("x is greater than 5") if x > 5 else print("x is less than or equal to 5") #output: x is less than or equal to 5

# 10. Lambda Functions:
add = lambda x, y: x + y
print(add(1, 2)) #output: 3

# 11. Generator Expressions:
squares = (x**2 for x in range(5))
print(list(squares)) #output: [0, 1, 4, 9, 16]

# 12. List Comprehension:
squares = [x**2 for x in range(5)]
print(squares) #output: [0, 1, 4, 9, 16]

even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(f"Even squares: {even_squares}") #output: Even squares: [4, 16, 36, 64, 100]

# 13. Dictionary Comprehension:
squares = {x: x**2 for x in range(5)}
print(squares) #output: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 14. Set Comprehension:
squares = {x**2 for x in range(5)}
print(squares) #output: {0, 1, 4, 9, 16}

# 15. Yield:
def gen():
    yield 1
    yield 2
    yield 3
for x in gen():
    print(x) #output: 1 2 3

# 16. Nonlocal:
def outer():
    x = 10
    def inner():
        nonlocal x
        x += 1
    inner()
    print(x) #output: 11

# 17. Global:
x = 10
def func():
    global x
    x += 1
func()
print(x) #output: 11


# 7. Functions:
# 7.1. Function Definition:
def add(a, b):
    return a + b
print(add(1, 2)) #output: 3

# 7.2. Function Arguments:
def greet(name, age):
    print(f"Hello, {name}! You are {age} years old.")
greet("Alice", 25) #output: Hello, Alice! You are 25 years old.

# 7.3. Default Arguments:
def greet(name, age=25):
    print(f"Hello, {name}! You are {age} years old.")
greet("Alice") #output: Hello, Alice! You are 25 years old.

# 7.4. Keyword Arguments:
def greet(name, age):
    print(f"Hello, {name}! You are {age} years old.")
greet(name="Alice", age=25) #output: Hello, Alice! You are 25 years old.

# 7.5. Variable-Length Arguments:
def add(*args):
    total = 0
    for num in args:
        total += num
    return total
print(add(1, 2, 3, 4, 5)) #output: 15

# 7.6. Arbitrary Keyword Arguments:
def greet(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
greet(name="Alice", age=25) #output: name: Alice age: 25

# 7.7. Function Return Values:
def add(a, b):
    return a + b
result = add(1, 2)
print(result) #output: 3

# 7.8. Lambda Functions:
add = lambda a, b: a + b
print(add(1, 2)) #output: 3

# 7.9. Recursive Functions:
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
print(factorial(5)) #output: 120

# 7.10. Docstrings:
def greet(name):
    """Greet a person by name."""
    print(f"Hello, {name}!")
greet("Alice") #output: Hello, Alice!
print(greet.__doc__) #output: Greet a person by name.

# 7.11. Built-in Functions:
print(abs(-5)) #output: 5
print(max(1, 2, 3)) #output: 3
print(min(1, 2, 3)) #output: 1
print(pow(2, 3)) #output: 8
print(round(3.14)) #output: 3
print(sum([1, 2, 3])) #output: 6

# 7.12. Modules:
import math
print(math.pi) #output: 3.141592653589793
print(math.sqrt(16)) #output: 4.0

# 7.13. Packages:
from math import pi, sqrt
print(pi) #output: 3.141592653589793
print(sqrt(16)) #output: 4.0

    
#8.Exception Handling:
# Try-except:
try:
    num = int(input("Enter a number: "))
    print(num)
except ValueError:
    print("Invalid input. Please enter a number.")
    
#example2:
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Error: Division by zero!") #output: Error: Division by zero!

# Try-except-else-finally:
try:
    num = int("10")
except ValueError:
    print("Invalid conversion")
else:
    print(f"Conversion successful: {num}")
finally:
    print("This always executes")
    
# 9. File Operations:

# Writing to a file
with open("sample.txt", "w") as file:
    file.write("Hello, Python!\n")
    file.write("File operations are essential.\n")

print("File written successfully")

# Reading from a file
try:
    with open("sample.txt", "r") as file:
        content = file.read()
        print("File content:")
        print(content)
except FileNotFoundError:
    print("File not found")

# 9.1. Reading a File:
f = open("sample.txt", "r")
content = f.read()
f.close()
print(content) #output: Hello, world!

# 9.2. Writing to a File:
f = open("sample.txt", "w")
f.write("Hello, world!")
f.close()

# 9.3. Appending to a File:
f = open("sample.txt", "a")
f.write("Hello, world!")
f.close()

# 9.4. Reading and Writing at the Same Time:
f = open("sample.txt", "r+")
f.write("Hello, world!")
f.close()

# 9.5. Using Context Manager:
with open("sample.txt", "w") as f:
    f.write("Hello, world!")



#removing the txt file after use
import os
import glob
from contextlib import contextmanager

@contextmanager
def find_and_remove_files(pattern):
    """
    Context manager that finds files matching a pattern in the current directory,
    yields a list of matching paths, and removes them after the context exits.
    """
    matching_files = glob.glob(pattern)
    
    try:
        yield matching_files
    finally:
        # Remove all matching files after context exits
        for file_path in matching_files:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")

# Example usage:
with find_and_remove_files("*.txt") as files:
    print(f"Found {len(files)} text files")
    for file_path in files:
        # Process each file before removal
        print(f"Processing: {file_path}")
        
        
        

"""    
# 9.6. Reading CSV Files:
import csv
with open("example.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        
# 9.7. Writing CSV Files:
import csv
with open("example.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age"])
    writer.writerow(["Alice", 25])
    writer.writerow(["Bob", 30])
    
# 9.8. Reading JSON Files:
import json
with open("example.json", "r") as f:
    data = json.load(f)
    print(data)
    
# 9.9. Writing JSON Files:
import json
data = {"name": "John", "age": 30}
with open("example.json", "w") as f:
    json.dump(data, f)
    
"""
    
    
# 10. Modules and Imports:

import math

print(f"Pi: {math.pi}") #output:=> Pi: 3.141592653589793
print(f"Square root of 16: {math.sqrt(16)}") #output:=> Square root of 16: 4.0

# Import specific functions
from random import randint, choice

print(f"Random number between 1 and 10: {randint(1, 10)}") #output:=> Random number between 1 and 10: 8
print(f"Random fruit: {choice(fruits)}") #output:=> Random fruit: apple



# 11. Regular Expressions:
import re

text = "The quick brown fox jumps over the lazy dog."
match = re.search(r"quick|fox|lazy", text)
if match:
    print("Match found:", match.group()) #output: Match found: quick
else:
    print("No match found") #Output:=> Match found: quick
    
    
    
# Basic pattern matching with re.findall() to extract email addresses
# Match at beginning of string with re.match() to validate if text starts with a date
# Search anywhere in a string with re.search() to find phone numbers
# Text substitution with re.sub() to redact sensitive information
# Text splitting with re.split() to parse CSV-like data

#Example:

# Import the re module
import re

# Basic pattern matching
text = "Contact us at info@example.com or support@company.org"
print(f"Original text: {text}") #output:=> Original text: Contact us at info@example.com or support@company.org

# Find all email addresses
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
emails = re.findall(email_pattern, text)
print(f"Found emails: {emails}") #output: Found emails: ['info@example.com', 'support@company.org']

# Match at beginning of string
date_text = "2023-05-15 is the deadline"
date_pattern = r'^\d{4}-\d{2}-\d{2}'
if re.match(date_pattern, date_text):
    print(f"Text starts with a date: {re.match(date_pattern, date_text).group()}") #output: Text starts with a date: 2023-05-15

# Search anywhere in the string
phone_text = "Call me at 555-123-4567 tomorrow"
phone_pattern = r'\d{3}-\d{3}-\d{4}'
phone_match = re.search(phone_pattern, phone_text)
if phone_match:
    print(f"Found phone number: {phone_match.group()}") #output: Found phone number: 555-123-4567
    
    
# Substitution
censored_text = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', "[EMAIL REDACTED]", text)
print(f"Censored text: {censored_text}") #output: Censored text: Contact us at [EMAIL REDACTED] or support@company

# Splitting text
csv_data = "Alice,25,New York;Bob,30,Chicago;Charlie,22,Los Angeles"
people = re.split(r';', csv_data)
print("Split data:")
for person in people:
    details = re.split(r',', person)
    print(f"- Name: {details[0]}, Age: {details[1]}, City: {details[2]}") 
#output:
# Split data:
# - Name: Alice, Age: 25, City: New York
# - Name: Bob, Age: 30, City: Chicago
# - Name: Charlie, Age: 22, City: Los Angeles


# Groups in regular expressions
log_entry = "127.0.0.1 - - [20/May/2023:10:12:25 -0400] \"GET /index.html HTTP/1.1\" 200 2048"
log_pattern = r'(\d+\.\d+\.\d+\.\d+).*\[([^\]]+)\].*\"([A-Z]+) ([^ ]+).*\" (\d+) (\d+)'
match = re.search(log_pattern, log_entry)

if match:
    print("Log entry parsed:")
    print(f"- IP Address: {match.group(1)}")
    print(f"- Timestamp: {match.group(2)}")
    print(f"- Method: {match.group(3)}")
    print(f"- Resource: {match.group(4)}")
    print(f"- Status code: {match.group(5)}")
    print(f"- Response size: {match.group(6)}")
    
    
#output:
# Log entry parsed:
# - IP Address: 127.0.0.1
# - Timestamp: 20/May/2023:10:12:25 -0400
# - Method: GET
# - Resource: /index.html
# - Status code: 200
# - Response size: 2048
    

 
     
# 12. Working with Dates and Times:

import datetime
date = datetime.date(2022, 1, 1)
time = datetime.time(12, 30, 0)
datetime_object = datetime.datetime(2022, 1, 1, 12, 30, 0) 
print(f"Date: {date}") #output:=> Date: 2022-01-01
print(f"Time: {time}") #output:=> Time: 12:30:00
print(f"Date and Time: {datetime_object}") #output:=> Date and Time: 2022-01-01 12:30:00



#Example:
# Import datetime modules
from datetime import datetime, date, time, timedelta
import time as time_module

# Current date and time
now = datetime.now()
print(f"Current date and time: {now}")
print(f"Formatted date: {now.strftime('%Y-%m-%d')}")
print(f"Formatted time: {now.strftime('%H:%M:%S')}")
print(f"Formatted date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}")


#output:

# Current date and time: 2025-05-06 06:02:47.591101
# Formatted date: 2025-05-06
# Formatted time: 06:02:47
# Formatted date and time: 2025-05-06 06:02:47

# Creating specific dates
birthday = date(1990, 5, 15)
print(f"Birthday: {birthday}")
print(f"Birthday (formatted): {birthday.strftime('%B %d, %Y')}")

#output:
# Birthday: 1990-05-15
# Birthday (formatted): May 15, 1990

# Creating specific times
alarm = time(7, 30, 0)
print(f"Alarm time: {alarm}")
print(f"Alarm (formatted): {alarm.strftime('%I:%M %p')}")

#output:
# Alarm time: 07:30:00
# Alarm (formatted): 07:30 AM

# Combining date and time
meeting = datetime.combine(date(2023, 8, 15), time(14, 30))
print(f"Meeting: {meeting}")

# Date arithmetic with timedelta
today = date.today()
print(f"Today: {today}")

one_week = timedelta(days=7)
next_week = today + one_week
print(f"One week from today: {next_week}")

three_hours = timedelta(hours=3)
later = now + three_hours
print(f"Three hours from now: {later}")

# Time differences
start_date = date(2023, 1, 1)
end_date = date(2023, 12, 31)
days_in_2023 = end_date - start_date
print(f"Days in 2023: {days_in_2023.days}")

# Parsing dates from strings
date_string = "2023-06-15 08:30:00"
parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(f"Parsed date: {parsed_date}")
print(f"Year: {parsed_date.year}, Month: {parsed_date.month}, Day: {parsed_date.day}")
print(f"Hour: {parsed_date.hour}, Minute: {parsed_date.minute}")

# Working with timestamps
current_timestamp = time_module.time()
print(f"Current timestamp (seconds since epoch): {current_timestamp}")

# Convert timestamp to datetime
timestamp_date = datetime.fromtimestamp(current_timestamp)
print(f"Timestamp as datetime: {timestamp_date}")



# Time zones (requires third-party package 'pytz')
# If pytz is installed, uncomment the following code:

"""
from datetime import datetime
import pytz

# Create timezone-aware datetime
utc_now = datetime.now(pytz.UTC)
print(f"Current UTC time: {utc_now}")

# Convert to a different timezone
ny_timezone = pytz.timezone('America/New_York')
ny_time = utc_now.astimezone(ny_timezone)
print(f"New York time: {ny_time}")

# List some available timezones
print("Some available timezones:")
for tz in sorted(pytz.common_timezones)[:5]:  # Show first 5 timezones
    print(f"- {tz}") 
    
"""


#Function Example:

#Calculate the age of a person after 5 years and print it with fstring

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


#or

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
    
######################### End of File #############################################