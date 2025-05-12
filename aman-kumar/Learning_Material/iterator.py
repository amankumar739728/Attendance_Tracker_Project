#Iterator:
##=> An iterator is an object that contains a countable number of values.(Lists, tuples, 
# dictionaries, and sets are all iterable objects.)
##=> __iter__() and __next__().

l1=[23,2,45,"Aman"]
myit = iter(l1)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))

#output:
# 23
# 2
# 45
# Aman

#StopIteration:
try:
  l1=[23,2,45,"Aman"]
  myit = iter(l1)

  print(next(myit))
  print(next(myit))
  print(next(myit))
  print(next(myit))
  print(next(myit))
except StopIteration as e:
  print("StopIteration Error")
finally:
  print("End of Program")
  
#output:
# 23
# 2
# 45
# Aman
# StopIteration Error
# End of Program



l1 = [23, 2, 45, "Aman"]
myit = iter(l1)

try:
    for item in myit:
        print(item)
except StopIteration:
    print("StopIteration Error")
finally:
    print("End of Program")
    
#output:
# 23
# 2
# 45
# Aman
# End of Program