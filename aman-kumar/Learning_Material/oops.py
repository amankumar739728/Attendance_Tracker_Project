#Class and Object:
# A class is a blueprint for creating objects. An object is an instance of a class.

# A class is a collection of objects. Classes are blueprints for creating objects. 
# A class defines a set of attributes and methods that the created objects (instances) can have.

# Some points on Python class:  

# Classes are created by keyword class.
# Attributes are the variables that belong to a class.

#Class and Function example with constructor(__init__ method) and object method (showres method)

class Person:
  def __init__(self,fname,lname,age):
    self.fname = fname
    self.lname = lname
    self.age = age
  def showres(self):
    fullname = self.fname+" "+self.lname
    print(f"Myself {fullname} age: {self.age}")
p1=Person('Aman','Kumar',25)
p1.showres()

#output: Myself Aman Kumar age: 25



#1.inheritance:

"""
# Inheritance is a mechanism in OOP that allows one class to inherit the attributes and methods of another class.
# It promotes code reusability and establishes a relationship between classes.
# Inheritance is a way to form new classes using classes that have already been defined.
# It allows us to create a new class that is a modified version of an existing class.
"""

class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

class Student(Person):
  def __init__(self, fname, lname,year):
    super().__init__(fname, lname)
    #or we can use below line:
    #Person.__init__(self,fname,lname)
    self.graduationyear = year

x = Student("Mike", "Olsen",2019)
x.printname()
print(x.graduationyear)


#output:
# Mike Olsen
# 2019


#inheritance:

class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    full_name = self.firstname+" "+self.lastname
    return f"Full Name: {full_name}" #to avoid none in the below output we are using return

class Student(Person):
  def __init__(self, fname, lname,year):
    super().__init__(fname, lname)
    #or we can use below line:
    #Person.__init__(self,fname,lname)
    self.graduationyear = year

x = Student("Mike", "Olsen",2019)
print(x.printname())
print(x.graduationyear)


#output:
# Full Name: Mike Olsen
# 2019



#Types of Inheritance:

"""
# Single Inheritance: A child class inherits from a single parent class.
# Multiple Inheritance: A child class inherits from more than one parent class.
# Multilevel Inheritance: A child class inherits from a parent class, which in turn inherits from another class.
# Hierarchical Inheritance: Multiple child classes inherit from a single parent class.
# Hybrid Inheritance: A combination of two or more types of inheritance.
"""

# Single Inheritance
class Dog:
    def __init__(self, name):
        self.name = name

    def display_name(self):
        print(f"Dog's Name: {self.name}")

class Labrador(Dog):  # Single Inheritance
    def sound(self):
        print("Labrador woofs")

# Multilevel Inheritance
class GuideDog(Labrador):  # Multilevel Inheritance
    def guide(self):
        print(f"{self.name}Guides the way!")

# Multiple Inheritance
class Friendly:
    def greet(self):
        print("Friendly!")

class GoldenRetriever(Dog, Friendly):  # Multiple Inheritance
    def sound(self):
        print("Golden Retriever Barks")

# Example Usage
lab = Labrador("Buddy")
lab.display_name()
lab.sound()

guide_dog = GuideDog("Max")
guide_dog.display_name()
guide_dog.guide()

retriever = GoldenRetriever("Charlie")
retriever.display_name()
retriever.greet()
retriever.sound()



#output:
# Dog's Name: Buddy
# Labrador woofs
# Dog's Name: Max
# MaxGuides the way!
# Dog's Name: Charlie
# Friendly!
# Golden Retriever Barks




#2.Polymorphism:

""""#Polymorphism is often used in Class methods, where we can have multiple classes
with the same method name."""


"""
#Polymorphism is a concept in OOP that allows objects of different classes to be 
treated as objects of a common superclass.
#It is a way to perform a single action in different forms.
#Polymorphism can be achieved through method overriding and operator overloading.
"""


class Car:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Drive!")

class Boat:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Sail!")

class Plane:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Fly!")

car1 = Car("Ford", "Mustang")       #Create a Car object
boat1 = Boat("Ibiza", "Touring 20") #Create a Boat object
plane1 = Plane("Boeing", "747")     #Create a Plane object

for x in (car1, boat1, plane1):
  x.move()
    


#output:
# Drive!
# Sail!
# Fly!


#3.Encapsulation:

"""
#Encapsulation is the bundling of data with the methods that operate on that data.
#Encapsulation is a protective barrier that keeps the data safe within the object and prevents outside code from directly accessing it.
#Encapsulation is achieved by using private and protected access modifiers.
#Private members are not accessible from outside the class.
#Protected members are accessible within the class and its subclasses.
"""

class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Insufficient funds")

    def get_balance(self):
        return self.__balance
      
# Create an instance of BankAccount
account = BankAccount(1000)
# Try to access the private attribute directly
print(account._BankAccount__balance)  # Output: 1000
# Deposit and withdraw money
account.deposit(500)
account.withdraw(200)
# Get the current balance
print(account.get_balance())

#output:
# 1000
# 1300



#Example using protected members:
class Animal:
    def __init__(self, name):
        self._name = name  # Protected attribute

    def make_sound(self):
        print(f"{self._name} makes a sound")

class Dog(Animal):
    def bark(self):
        print(f"{self._name} barks")
        
# Create an instance of Dog
dog = Dog("Buddy")
# Try to access the protected attribute directly
print(dog._name)  # Output: Buddy
# Make sound and bark
dog.make_sound()  # Output: Buddy makes a sound
dog.bark()        # Output: Buddy barks 




#4.Abstraction:

"""Abstraction is a concept in object-oriented programming that allows 
you to show only the necessary information to the outside world while
hiding the implementation details."""

#Abstraction can be achieved using abstract classes and interfaces.

#Example:

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
      area = self.width * self.height
      return f"Area of Rectangle: {area}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        area = 3.14 * self.radius * self.radius
        return f"Area of Circle: {area}"

# Create an instance of Rectangle
rect = Rectangle(10, 20)
# Calculate the area
print(rect.area())  # Output: 200

# Create an instance of Circle
circle = Circle(5)
# Calculate the area
print(circle.area())  # Output: 78.5

#output:
# Area of Rectangle: 200
# Area of Circle: 78.5







