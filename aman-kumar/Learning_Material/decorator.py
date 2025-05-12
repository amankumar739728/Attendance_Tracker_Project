def simple_decorator(func):
    def wrapper():
        print("Before calling the function.")
        func()
        print("After calling the function.")
    return wrapper

@simple_decorator
def greet():
    print("Hello, World!")

greet()

#output:
# Before calling the function.
# Hello, World!
# After calling the function.



#pass function as an argument

def add(x, y):
    return x + y
def subtract(x, y):
    return x - y
def multiply(x, y):
    return x * y
def divide(x, y):
    return x / y

def calculate(func, x, y):
    return func(x, y)

result = calculate(add, 4, 6)
result1= calculate(subtract, 10, 5)
result2 = calculate(multiply, 2, 3)
result3 = calculate(divide, 10, 2)
print(f"result:{result}")
print(f"result1:{result1}")
print(f"result2:{result2}")
print(f"result3:{result3}")

#Output:
#result:10
#result1:5
# result2:6
# result3:5.0


#Example:
def decorator_function(original_function):
    def wrapper_function():
        print("\ndecorator function is running")
        print("Wrapper executed before {} Method".format(original_function.__name__))
        return original_function()
    return wrapper_function
@decorator_function
def display():
    print("Display function executed")
display()


#output:
# Wrapper executed before display
# Display function executed


#Example 2:
def make_pretty(func):
    # define the inner function 
    def inner():
        # add some additional behavior to decorated function
        print("\nDecorator example")
        print("I got decorated")

        # call original function
        func()
    # return the inner function
    return inner

# define ordinary function
def ordinary():
    print("I am ordinary")
    
# decorate the ordinary function
decorated_func = make_pretty(ordinary)

# call the decorated function
decorated_func()


#--->using decorator(@)
def make_pretty(func):

    def inner():
        print("\nInside the inner function of example 2")
        print("I got decorated")
        func()
    return inner

@make_pretty
def ordinary():
    print("I am ordinary")

ordinary()  
