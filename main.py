import sys
from graph import build_graph

def main():
    if len(sys.argv) == 3:
        json_file = sys.argv[1]
        os = sys.argv[2]
    else:
        print("No json file provided")
        quit()

    build_graph(json_file, os)


if __name__ == "__main__":
    main()