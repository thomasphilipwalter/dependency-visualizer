import json
import sys

def get_dependencies(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    packages = data["Packages"]

    return packages

def clean_data(data, os):

    data_cleaned = {}

    for package, details in data.items():
        data_cleaned[package] = set()

        if os == "mac":
            all_items = details.get('Requirements', [])
        else: 
            all_items = details.get('Imports', []) + details.get('LinkingTo', []) + details.get('Depends', [])

        for item in all_items:
            item_name = item.split(maxsplit=1)[0]
            data_cleaned[package].add(item_name)
    
    return data_cleaned

def main():
    if len(sys.argv) == 2:
        json_file = sys.argv[1]
    else:
        print("No json file provided")
        quit()

    packages = get_dependencies(json_file)
    print(packages)

if __name__ == "__main__":
    main()