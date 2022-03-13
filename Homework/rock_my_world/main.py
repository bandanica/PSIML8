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
    famousCities={}
    avgCities={}
    numConCity = {}
    avgA = 0
    ukupno=0
    numKonc=0
    prazneVen = {}
    ukupnoVen = {}
    nVen={}
    brojPosBend={}
    brojKoncBend = {}
    prosekBend={}

    mapaPodataka = {}
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
        mapaPodataka[file] = data
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
        venue = g + "\\" + file[t + 1]
        if g not in cities.keys():
            cities[g] = len(data)
        else:
            cities[g] = cities[g] + len(data)

        att = [x for x in data if "is_indie" in x.keys() and x["is_indie"]==True]

        #AKO NEMA BROJA ATTENDANCE, STAVLJA SE PROSEK ZA TAJ VENUE, AKO NEMA DRUGIH KONCERATA,
        #STAVLJA SE PROSEK ZA TAJ GRAD CEO(SVE VENUE U FOLDERU)
        #prosek = sum(x["attendance"] for x in att if "attendance" in x.keys())
        #if prosek!=0:
        #    prosek/=sum(1 for x in att if "attendance" in x.keys())


        for con in data:
            if not "attendance" in con.keys():
                #if prosek!=0:
                #    con["attendance"] = prosek
                #else:
                con["attendance"]=-1

                if con in att:
                    if g not in avgCities.keys():
                        avgCities[g] = 1
                    else:
                        avgCities[g] +=1
                    if venue not in prazneVen.keys():
                        prazneVen[venue] = 1
                    else:
                        prazneVen[venue] +=1

        ukupno += sum(x["attendance"] for x in data if x["attendance"]!=-1)
        numKonc+= sum(1 for x in data if x["attendance"]!=-1)
        if g not in famousCities.keys():
            famousCities[g] = sum(x["attendance"] for x in att if x["attendance"]!=-1)
            numConCity[g] = sum(1 for x in att if x["attendance"]!=-1)

        else:
            famousCities[g] = famousCities[g] + sum(x["attendance"] for x in att if x["attendance"]!=-1)
            numConCity[g] += sum(1 for x in att if x["attendance"]!=-1)
        if venue not in nVen.keys():
            nVen[venue] = sum(1 for x in data if x["attendance"]!=-1)
            ukupnoVen[venue] = sum(x["attendance"] for x in data if x["attendance"]!=-1)
        else:
            nVen[venue] += sum(1 for x in data if x["attendance"] != -1)
            ukupnoVen[venue] += sum(x["attendance"] for x in data if x["attendance"] != -1)

    for v in ukupnoVen.keys():
        if v in prazneVen.keys():
            if nVen[v]!=0:
                aver = ukupnoVen[v]/nVen[v]
                grad = v.split("\\")[0]
                famousCities[grad]+=prazneVen[v]*aver
                avgCities[grad]-=prazneVen[v]
                if avgCities[grad]<0:
                    avgCities[grad] = 0
    average = ukupno / numKonc

    for g in famousCities.keys():
        if g in avgCities.keys():
            #average = famousCities[g]/numConCity[g]

            famousCities[g]+=average*avgCities[g]

    for key,pod in mapaPodataka.items():
        x = sum(1 for x in pod if "is_indie" in x.keys() and x["is_indie"]==True)
        if (x>0):
            for data in pod:
                if data["attendance"]==-1:
                    ven = key.split("\\")
                    ven = ven[-2] + "\\" + ven[-1]
                    if ven in ukupnoVen.keys() and nVen[ven]!=0:
                        data["attendance"] = ukupnoVen[ven]/nVen[ven]
                    else:
                        data["attendance"] = average
                if data["band_name"] not in brojPosBend.keys():
                    brojPosBend[data["band_name"]]=data["attendance"]
                    brojKoncBend[data["band_name"]] = 1
                else:
                    brojPosBend[data["band_name"]]+=data["attendance"]
                    brojKoncBend[data["band_name"]]+=1

    #for bendovi in brojPosBend.keys():
    #    prosekBend[bendovi] = brojPosBend[bendovi]/brojKoncBend[bendovi]
    prosekBend = {bendovi:brojPosBend[bendovi]/brojKoncBend[bendovi] for bendovi in brojPosBend.keys()}


    town = {key:value for (key,value) in cities.items() if cities[key]==max(cities.values())}
    return len(countries), sorted(town)[0], sorted(famousCities, key=famousCities.get, reverse=True)[:3], sorted(prosekBend, key=prosekBend.get, reverse=True)[:3]

if __name__ == "__main__":
    root_path = input()
    start_time = time.time()
    json_files = glob.glob(root_path + "/**/*.json", recursive=True)
    nc,city, famCities, bendovi = countryNumbers(json_files)
    print(np.size(json_files))
    print(nc)
    print(city)
    print(famCities)
    print(bendovi)
    print("--- %s seconds ---" % (time.time() - start_time))