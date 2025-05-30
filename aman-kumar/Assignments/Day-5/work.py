#(Question 13.): reading and writing to a file using pathlib and glob module

import glob
from pathlib import Path

# Define the target directory
target_dir = 'textdir/text_files/folder'

print("\nUsing glob:")
# Get list of .txt files using glob
for filepath in glob.glob(f'{target_dir}/*.txt'):
    with open(filepath, 'r') as file:
        line_count = sum(1 for _ in file)
    print(f"{filepath}: {line_count} lines")

print("\nUsing pathlib:")
# Get list of .txt files using pathlib
path = Path(target_dir)
for filepath in path.glob('*.txt'):
    with open(filepath, 'r') as file:
        line_count = sum(1 for _ in file)
    print(f"{filepath}: {line_count} lines")

#output:
# Using glob:
# textdir/text_files/folder\file1.txt: 1 lines
# textdir/text_files/folder\log.txt: 1 lines

# Using pathlib:
# textdir\text_files\folder\file1.txt: 1 lines
# textdir\text_files\folder\log.txt: 1 lines


#(Question 14.): optimize the code using dict comprehension

from typing import Dict

import requests
test_url = "https://reqres.in/api/users/2"
response = requests.get(test_url)
product_data = response.json()

def get_additional_data(style_number, sku_id):
    additional_data_temp = {'style_number': style_number, 'sku_id': sku_id, 'support': "test_support_data"}
    return additional_data_temp

additional_data: Dict = get_additional_data("CWS10", 10)

def pre_process_data():
    for field in additional_data:
        if field != 'support':
            product_data[field] = additional_data[field]
    return product_data

print(pre_process_data())


#optimized code using dict comprehension
from typing import Dict
import requests
test_url = "https://reqres.in/api/users/2"
response1 = requests.get(test_url)
product_data = response1.json()
#optimized code using dict comprehension
additional_data = {'style_number': "CWS10", 'sku_id': 10, 'support': "test_support_data"}
product_data = {k: v for k, v in additional_data.items() if k != 'support'}
product_data.update(additional_data)
print(product_data)

    
