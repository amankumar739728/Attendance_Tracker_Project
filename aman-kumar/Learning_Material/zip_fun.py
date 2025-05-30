"""
zip() is a built-in Python function that combines multiple iterables 
(like lists, tuples, etc.) into pairs (or tuples) element-wise.

"""

names = ['Alice', 'Bob', 'Charlie']
scores = [85, 90, 95]

for name, score in zip(names, scores):
    print(f"{name} scored {score}")
    
    
#output:
# Alice scored 85
# Bob scored 90
# Charlie scored 95

#Note: In the above example, the zip() function pairs each name with its corresponding score.


#Example 2: 

print("\nlist of tuples:")
print(list(zip(names, scores)))

#output:
# list of tuples:
# [('Alice', 85), ('Bob', 90), ('Charlie', 95)]