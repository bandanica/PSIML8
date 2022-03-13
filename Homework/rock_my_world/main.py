# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

import glob
import numpy as np

def countJsonFiles(root_path):
    json_files = glob.glob(root_path + "/**/*.json", recursive=True)
    return json_files

if __name__ == "__main__":
    root_path = input()
    #dataset = root_path.split("/")[-1]
    print(np.size(countJsonFiles(root_path)))
    print()
    print()
    print()
    print()
