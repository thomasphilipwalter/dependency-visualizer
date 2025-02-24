import json
import sys

def get_dependencies(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    packages = data["Packages"]

    return packages

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