#method overloading:
#Python doesn't support method overloading directly like Java or C++. If you define multiple methods with the same name in a class, the last definition overwrites the previous ones.

class Calculator:
    def add(self, *args):
        return sum(args)

calc = Calculator()
print(calc.add(2, 3))         # Output: 5
print(calc.add(1, 2, 3, 4))   # Output: 10


#method overriding:
## Method overriding occurs when a child class provides a specific 
# implementation of a method that is already defined in its parent class.

class Animal:
    def sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def sound(self):  # Overriding parent class method
        print("Dog barks")

a = Animal()
a.sound()   # Output: Animal makes a sound

d = Dog()
d.sound()   # Output: Dog barks


# | Feature              | Method Overloading                          | Method Overriding                   |
# | -------------------- | ------------------------------------------- | ----------------------------------- |
# | Definition           | Same method name, different parameters      | Same method name, same parameters   |
# | Supported in Python? | No (but can mimic with default args/\*args) | Yes                                 |
# | Belongs to           | Same class                                  | Parent-child (inheritance)          |
# | Purpose              | Increase flexibility                        | Change behavior of inherited method |


# Example of method overloading using default arguments
class MathOperations:
    def multiply(self, a, b=1):
        return a * b

    def multiply(self, a, b, c):
        return a * b * c    

math = MathOperations()
print(math.multiply(2))  # Output: 2
print(math.multiply(2, 3))  # Output: 6
print(math.multiply(2, 3, 4))  # Output: 24

# Example of method overriding
class Parent:
    def greet(self):
        print("Hello from Parent")

class Child(Parent):
    def greet(self):
        print("Hello from Child")

parent = Parent()
parent.greet()  # Output: Hello from Parent
child = Child()
child.greet()  # Output: Hello from Child
