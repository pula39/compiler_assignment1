import sys
from classes import *

def main(file_path):
    literal_list = []
    with open(file_path, mode="r") as f:
        literal_list = f.read()

    print(literal_list)

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("plaese pass file path")
        sys.exit()

    file_path = sys.argv[1]

    print("File path : " + file_path)

    main(file_path)

