import sys
from graph import build_graph

def main():
    if len(sys.argv) == 2:
        json_file = sys.argv[1]
    else:
        print("No json file provided")
        quit()

    build_graph(json_file)


if __name__ == "__main__":
    main()