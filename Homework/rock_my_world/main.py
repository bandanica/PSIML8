# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def countJsonFiles(dataset):
    return dataset

if __name__ == "__main__":
    root_path = input()
    dataset = root_path.split("/")[-1]
    x = countJsonFiles(dataset)
