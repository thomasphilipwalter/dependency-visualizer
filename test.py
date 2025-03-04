import sys
import json

json_file = sys.argv[1]

with open(json_file, 'r') as file:
    data = json.load(file)

for item in data:
    print(type(item))
    print(item)
    print(type(item['package']))
    print(item['package'])
    print()
