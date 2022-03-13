# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

import glob
import numpy as np
import json
import os
import time

def countJsonFiles(root_path):
    json_files = glob.glob(root_path + "/**/*.json", recursive=True)
    return json_files

def countryNumbers(json_files):
    countries = set()
    cities={}
    for file in json_files:
        # proveravanje da li je koncert validan
        data = []
        if os.path.getsize(file) == 0:
            # print('empty')
            # print(file)
            continue
        with open(file) as f:
            if f.read()[0] == '[':
                # standard json format
                f = open(file)
                data = json.load(f)
            else:
                # newline delimiter format
                f = open(file, "r")
                data = f.readlines()
                for i, line in enumerate(data):
                    data[i] = json.loads(line.replace("\n", ""))

        # print(data)
        if not data:
            continue

        # remove concerts without band_name
        data = [x for x in data if "band_name" in x.keys()]
        # print(data)

        # rastavljanje putanje
        file = file.replace(root_path, '').split('\\')
        # file = file.split('\\')

        # racunanje zemalja sa bar jednim validnim koncertom

        # nalazenje zemlje u putanji
        # print(file)

        if file[1].split('_')[0].isnumeric() or file[1].split('-')[0].isnumeric():
            if file[2].split('_')[0].isnumeric() or file[2].split('-')[0].isnumeric():
                d = 4
            else:
                d = 2
        else:
            d = 1


        #PROVERITI DA LI TREBA .lower da se dodaje ili ne
        c = file[d].replace('-', '_')
        if (c.split("_")[0] == "the"):
            c = c.replace("the_", "", 1)
        countries.add(c)

        t = d+1
        g = file[t].replace('-', '_')
        if (g.split("_")[0] == "the"):
            g = g.replace("the_", "", 1)
        if g not in cities.keys():
            cities[g] = len(data)
        else:
            cities[g] = cities[g] + len(data)

    town = [x for x in sorted(cities) if cities[x]==max(cities.values())]
    return len(countries), town[0]

if __name__ == "__main__":
    root_path = input()
    start_time = time.time()
    json_files = glob.glob(root_path + "/**/*.json", recursive=True)
    nc,city = countryNumbers(json_files)
    print(np.size(json_files))
    print(nc)
    print(city)
    print()
    print()
    print("--- %s seconds ---" % (time.time() - start_time))