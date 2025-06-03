#decorator
def simple_decorator(func):
    def wrapper():
        print('before calling func')
        func()
        print('after calling func')
    return wrapper
    
@simple_decorator
def display():
    print('Hello Aman!')
    
display()

#output:
# before calling func
# Hello Aman!
# after calling func
    
def sum(a,b):
    return a+b
def subtract(a,b):
    return a-b
    
def calc(fun,a,b):
    return fun(a,b)
    
print(calc(sum,2,3))
        


l1=[3,4,5,1]
print(sorted(l1))


user_inp=input("enter ele sep by space: ")
list1=list(map(int,user_inp.split()))

n=len(list1)
for i in range(n):
    for j in range(i+1,n):
        if list1[i] > list1[j]:
            list1[i],list1[j] = list1[j],list1[i]
            
print("Sorted list:", list1)


#method overloading:
#Python doesn't support method overloading directly like Java or C++. If you define multiple methods with the same name in a class, the last definition overwrites the previous ones.

class Calculator:
    def add(self, *args):
        return sum(args)

calc = Calculator()
print(calc.add(2, 3))         # Output: 5
print(calc.add(1, 2, 3, 4))   # Output: 10


#method overriding:
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


#Inheritance:

class Person:
    def __init__(self,fname,lname):
        self.fname=fname
        self.lname=lname
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