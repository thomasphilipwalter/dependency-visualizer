from parse import get_dependencies
import sys

if len(sys.argv) != 3:
    print("need json file and OS")
    sys.exit()

json_file = sys.argv[1]
os = sys.argv[2]

data = get_dependencies(json_file)
tally = {}

for package, details in data.items():
    if os == "mac":
        all_items = details.get('Requirements', [])
    else:
        all_items = details.get('Imports', []) + details.get('LinkingTo', []) + details.get('Depends', [])

    all_items_unique = set()
    for item in all_items:
        item_name = item.split(maxsplit=1)[0]
        all_items_unique.add(item_name)

    
    if package not in tally:
        tally[package] = [len(all_items_unique), 0]
    else:
        tally[package][0] = len(all_items_unique)

    # Strip package names and count dependencies
    for item in all_items_unique:
        if item not in tally:
            tally[item] = [0, 0]
        tally[item][1] += 1

format = []
for key, value in tally.items():
    format.append((key, value[0], value[1], value[1] - value[0]))

format.sort(key=lambda x: x[3])

print("Package, No. dependencies, No. packages dependent, diff")
for item in format:
    print(f"{item[0]}, {item[1]}, {item[2]}, {item[3]}")

