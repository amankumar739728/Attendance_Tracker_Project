# File Operations:

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

# 1. Reading a File:
f = open("sample.txt", "r")
content = f.read()
f.close()
print(content) #output: Hello, world!

# 2. Writing to a File:
f = open("sample.txt", "w")
f.write("Hello, world!")
f.close()

# 3. Appending to a File:
f = open("sample.txt", "a")
f.write("Hello, world!")
f.close()

# 4. Reading and Writing at the Same Time:
f = open("sample.txt", "r+")
f.write("Hello, world!")
f.close()

# 5. Using Context Manager:
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