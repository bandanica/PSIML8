# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


from PIL import Image
from PIL import ImageOps
import numpy as np
import glob
import time

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
def moze(tabela, row, col, val):
    for j in range(0, 9):
        if tabela[row][j] == val:
            return False

    for i in range(0, 9):
        if tabela[i][col] == val:
            return False

    startRow = (row // 3) * 3
    startCol = (col // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if tabela[startRow+i][startCol+j] == val:
                return False

    return True

def ispisResenog(tabela):
   for row in tabela:
       print(",".join([str(int(x)) for x in row]))

def main():
    dir_path = input()
    start_time=time.time()
    img_path = glob.glob(dir_path + "/*.png", recursive=True)[0]
    digits_path = glob.glob(dir_path + "\\digits/*.png", recursive=True)

    # slike brojeva
    cifre = {}
    j = 0
    for path in digits_path:
        j += 1
        img = Image.open(path)
        novaslika = Image.new("RGB", img.size, (255, 255, 255))
        novaslika.paste(img, mask=img.split()[3])
        img = ImageOps.grayscale(novaslika)

        # pikseli = np.array(img)
        cifre[j] = img

    # print(img_path)
    img = ImageOps.grayscale(Image.open(img_path))

    pikseli = np.array(img)
    beliPikseli = np.array(np.where(pikseli == 255))
    # pocetni i krajnji pikseli u okviru kojih je tabla sudokua
    x1, y1, x2, y2 = beliPikseli[:, 0][0], beliPikseli[:, 0][1], beliPikseli[:, -1][0], beliPikseli[:, -1][1]
    # pikseli1 = pikseli[x1][y1:y2]
    # print(np.shape(pikseli1))
    # #print(pikseli1)
    # print(np.array(np.where(pikseli1==0)))
    # return
    n = x2 - x1 +1
    tabla = np.zeros((9, 9))
    # print(x1,x2,y1,y2)
    # print(x2-x1,y2-y1)
    i = 0
    while (n % 9 != 0):
        i += 1
        n = n - 10

    kvadr = int(n / 9)
    kvadrp=kvadr
    #print(kvadr)
    for j in cifre.keys():
        cifre[j] = cifre[j].resize((kvadr-2, kvadr-2))
        cifre[j] = ~np.array(cifre[j])

    razlike = {}
    rotacija = -1
    b=0
    for x in range(9):
        for y in range(9):
            startX = x1 + x * kvadrp + x * i + (x >= 3) * i + (x >= 6) * i
            stopX = x1 + x * kvadrp + x * i + (x >= 3) * i + (x >= 6) * i + kvadrp
            startY = y1 + y * kvadrp + y * i + (y >= 3) * i + (y >= 6) * i
            stopY = y1 + y * kvadrp + y * i + (y >= 3) * i + (y >= 6) * i + kvadrp
            p = pikseli[np.arange(startX, stopX), :][:, np.arange(startY, stopY)]
            p[p >= 125] = 255
            p[p < 125] = 0

            if (np.sum(p == 255)) ==  kvadr * kvadr:
                razlike[(x, y)] = (0, 0)

            else:
                #vert = p[:, int(kvadr / 2) - 1]
                #hort = p[int(kvadr / 2) - 1, :]
                kropuj = np.array(np.where(p == 0))
                # pocetni i krajnji pikseli u okviru kojih je tabla sudokua
                kropuj = min(kropuj[:, 0][0],min(kropuj[1,:]))
                #Image.fromarray(p).show()
                if (kropuj > 0):
                    p = np.array(Image.fromarray(p).crop((kropuj, kropuj, kvadr - kropuj, kvadr - kropuj)))
                    #Image.fromarray(p).show()
                    #return
                    cnove = {}
                    for j in cifre.keys():
                        cnove[j] = np.copy(cifre[j])
                        cnove[j] = np.array(Image.fromarray(cnove[j]).resize((kvadr - 2 * kropuj, kvadr - 2 * kropuj)))
                        cnove[j][cnove[j] >= 125] = 255
                        cnove[j][cnove[j] < 125] = 0
                        # cnove[j].resize((kvadr-2*kropuj, kvadr-2*kropuj))
                else:
                    cnove = cifre
                #Image.fromarray(p).show()

                p = ~p
                # if (x >= 3 and x <= 5):
                #     Image.fromarray(p).show()
                #     return
                for j in cnove.keys():
                    if rotacija == -1 and j!=6 and j!=9:

                        r1 = max(np.sum(np.abs(p - cnove[j])), np.sum(np.abs(cnove[j] - p)))
                        k = Image.fromarray(cnove[j])

                        r2 = max(np.sum(np.abs(p - np.array(k.rotate(90)))), np.sum(np.abs(np.array(k.rotate(90)) - p)))
                        r3 = max(np.sum(np.abs(p - np.array(k.rotate(180)))),
                                 np.sum(np.abs(np.array(k.rotate(180)) - p)))
                        r4 = max(np.sum(np.abs(p - np.array(k.rotate(270)))),
                                 np.sum(np.abs(np.array(k.rotate(270)) - p)))
                        niz = [r1, r2, r3, r4]
                        if (min(niz)) < (255 * np.shape(p)[0] * np.shape(p)[1] * 0.01):
                            # print(255*0.01*np.shape(p)[0]*np.shape(p)[1])
                            # #print(np.shape(p))
                            # #print("usao")
                            # #k.rotate(90).show()
                            # Image.fromarray(p).show()
                            # Image.fromarray(p - np.array(k)).show()
                            # Image.fromarray(np.array(k) - p).show()
                            # print(niz)
                            # return
                            if (r1 == min(niz)):
                                rotacija = 0
                            elif (r2 == min(niz)):
                                rotacija = 90
                                cnove[j] = np.array(Image.fromarray(cnove[j]).rotate(90))

                            elif (r3 == min(niz)):
                                rotacija = 180
                                cnove[j] = np.array(Image.fromarray(cnove[j]).rotate(180))
                            else:
                                rotacija = 270
                                cnove[j] = np.array(Image.fromarray(cnove[j]).rotate(270))

                    elif rotacija!=-1:
                        cnove[j] = np.array(Image.fromarray(cnove[j]).rotate(rotacija))
                        #print(rotacija)
                        #Image.fromarray(cnove[j]).show()
                        #return
                    if (x==0 and (y==0 or y==1) and j==9 and rotacija==-1):
                        b+=1

                    if rotacija != -1:
                        if (x, y) not in razlike.keys():
                            razlike[(x, y)] = (max(np.sum(np.abs(p - cnove[j])), np.sum(np.abs(cnove[j]) - p)), j)
                        elif max(np.sum(np.abs(p - cnove[j])), np.sum(np.abs(cnove[j]) - p)) < razlike[(x, y)][0]:
                            razlike[(x, y)] = (max(np.sum(np.abs(p - cnove[j])), np.sum(np.abs(cnove[j]) - p)), j)


                # Image.fromarray(p-cnove[razlike[(x,y)][1]]).show()
                if rotacija==0:
                    tabla[x, y] = razlike[(x, y)][1]
                elif rotacija==180:
                    tabla[8-x,8-y] = razlike[(x,y)][1]
                elif rotacija==270:
                    tabla[8-y,x] =razlike[(x,y)][1]
                elif rotacija==90:
                    tabla[y,8-x] = razlike[(x,y)][1]
                #else:
                #    tabla[y,8-y] = razlike[(x,y)][1]

    for sestdevet in range(b):
        startX = x1
        stopX = x1 + kvadrp
        startY = y1 + sestdevet * kvadrp + sestdevet * i + (sestdevet >= 3) * i + (sestdevet >= 6) * i
        stopY = y1 + sestdevet * kvadrp + sestdevet * i + (sestdevet >= 3) * i + (sestdevet >= 6) * i + kvadrp
        p = pikseli[np.arange(startX, stopX), :][:, np.arange(startY, stopY)]
        p[p >= 125] = 255
        p[p < 125] = 0

        kropuj = np.array(np.where(p == 0))
        # pocetni i krajnji pikseli u okviru kojih je tabla sudokua
        kropuj = min(kropuj[:, 0][0], min(kropuj[1, :]))
        # Image.fromarray(p).show()
        if (kropuj > 0):
            p = np.array(Image.fromarray(p).crop((kropuj, kropuj, kvadr - kropuj, kvadr - kropuj)))
            # Image.fromarray(p).show()
            # return
            cnove = {}
            for j in cifre.keys():
                cnove[j] = np.copy(cifre[j])
                cnove[j] = np.array(Image.fromarray(cnove[j]).resize((kvadr - 2 * kropuj, kvadr - 2 * kropuj)))
                cnove[j][cnove[j] >= 125] = 255
                cnove[j][cnove[j] < 125] = 0
                # cnove[j].resize((kvadr-2*kropuj, kvadr-2*kropuj))
        else:
            cnove = cifre

        p=~p
        #Image.fromarray(p).show()
        for j in range(6,10,3):

            # cnove[j]=~cnove[j]
            #Image.fromarray(cnove[j]).rotate(rotacija).show()

            cnove[j] = np.array(Image.fromarray(cnove[j]).rotate(rotacija))
            #print(max(np.sum(np.abs(p - cnove[j])), np.sum(np.abs(cnove[j]) - p)))
            #Image.fromarray(cnove[j]-p).show()
            #Image.fromarray(p-cnove[j]).show()
            if (0, sestdevet) not in razlike.keys():
                #print("uslo1")
                razlike[(0, sestdevet)] = (max(np.sum(np.abs(p - cnove[j])), np.sum(np.abs(cnove[j]) - p)), j)

            elif max(np.sum(np.abs(p - cnove[j])), np.sum(np.abs(cnove[j]) - p)) < razlike[(0, sestdevet)][0]:
                #print("uslo2")
                razlike[(0, sestdevet)] = (max(np.sum(np.abs(p - cnove[j])), np.sum(np.abs(cnove[j]) - p)), j)
        if rotacija == 0:
            tabla[0, sestdevet] = razlike[(0, sestdevet)][1]
        elif rotacija == 180:
            tabla[8 - 0, 8 - sestdevet] = razlike[(0, sestdevet)][1]
        elif rotacija == 270:
            tabla[8 - sestdevet, 0] = razlike[(0, sestdevet)][1]
        elif rotacija == 90:
            tabla[sestdevet, 8 - 0] = razlike[(0, sestdevet)][1]

    #print(rotacija)
    #print(tabla)
    resavanje=np.copy(tabla)
    #resavanje sudokua
    #https://python.plainenglish.io/solve-a-sudoku-puzzle-using-backtracking-in-python-8e9eb58e57e6
    def resi():
        for i in range(0, 9):
            for j in range(0, 9):
                if resavanje[i][j] == 0:
                    for val in range(1, 10):
                        if moze(resavanje, i, j, val):
                            resavanje[i][j] = val
                            resi()

                            resavanje[i][j] = 0
                    return

        ispisResenog(resavanje)



    for row in tabla:
        print (",".join([str(int(x)) for x in row]))
    resi()
    #for row in tabla:
    #    print(",".join([str(int(x)) for x in row]))

    print("--- %s seconds ---" % (time.time() - start_time))
    img.close()


if __name__ == "__main__":
    main()
