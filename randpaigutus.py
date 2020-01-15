from random import randint, choice
from copy import deepcopy
from time import time
import os



dir1 = "./boarddata"
try:
    os.listdir(dir1)
except:
    os.mkdir(dir1)

def paiguta(n):
    global valmis
    global arvutil
    global kaua
    pikkus = laevapikkused.pop()
    saab = False
    kaua = False
    if time() - algaeg > 2:
        kaua = True
        return None
    if pikkus == 1:
        voim = [[a,b,1] for a in range(0,11-pikkus) for b in range(0,10)]
    else:
        voim = [[a,b,c] for a in range(0,11-pikkus) for b in range(0,10) for c in range(0,2)]
    #print(voim)
    eelmised[n] = deepcopy(arvutil)
    valmis = False
    while voim:
        arvutil = deepcopy(eelmised[n])
        valik = choice(voim)
        voim.remove(valik)
        #print(voim)
        #print(len(voim))
        alg1 = valik[0]
        alg2 = valik[1]
        suund = valik[2]
        if suund == 0:
            x, y = alg1, alg2
        else:
            x, y = alg2, alg1
        #print(n)
        #print(x,y,suund,pikkus)
        #for i in arvutil:
            #print(i)
        saab = True
        if suund == 0:
            for i in range(pikkus):
                if arvutil[y][x+i] in [1,"x"]:
                    saab = False
                    break
        else:
            for i in range(pikkus):
                if arvutil[y+i][x] in [1,"x"]:
                    saab = False
                    break
        if saab:
            if suund == 0:
                for i in range(pikkus):
                    arvutil[y][x+i] = 1
                if y > 0:
                    for i in range(pikkus):
                        if arvutil[y-1][x+i] != 1:
                            arvutil[y-1][x+i] = "x"
                if y < 9:
                    for i in range(pikkus):
                        if arvutil[y+1][x+i] != 1:
                            arvutil[y+1][x+i] = "x"
                if x > 0:
                    if arvutil[y][x-1] != 1:
                        arvutil[y][x-1] = "x"
                    if y > 0:
                        if arvutil[y-1][x-1] != 1:
                            arvutil[y-1][x-1] = "x"
                    if y < 9:
                        if arvutil[y+1][x-1] != 1:
                            arvutil[y+1][x-1] = "x"
                if x + pikkus <= 9:
                    if arvutil[y][x+pikkus] != 1:
                        arvutil[y][x+pikkus] = "x"
                    if y > 0:
                        if arvutil[y-1][x+pikkus] != 1:
                            arvutil[y-1][x+pikkus] = "x"
                    if y < 9:
                        if arvutil[y+1][x+pikkus] != 1:
                            arvutil[y+1][x+pikkus] = "x"
            else:
                for i in range(pikkus):
                    arvutil[y+i][x] = 1
                if x > 0:
                    for i in range(pikkus):
                        if arvutil[y+i][x-1] != 1:
                            arvutil[y+i][x-1] = "x"
                if x < 9:
                    for i in range(pikkus):
                        if arvutil[y+i][x+1] != 1:
                            arvutil[y+i][x+1] = "x"
                if y > 0:
                    if arvutil[y-1][x] != 1:
                        arvutil[y-1][x] = "x"
                    if x > 0:
                        if arvutil[y-1][x-1] != 1:
                            arvutil[y-1][x-1] = "x"
                    if x < 9:
                        if arvutil[y-1][x+1] != 1:
                            arvutil[y-1][x+1] = "x"
                if y + pikkus <= 9:
                    if arvutil[y+pikkus][x] != 1:
                        arvutil[y+pikkus][x] = "x"
                    if x > 0:
                        if arvutil[y+pikkus][x-1] != 1:
                            arvutil[y+pikkus][x-1] = "x"
                    if x < 9:
                        if arvutil[y+pikkus][x+1] != 1:
                            arvutil[y+pikkus][x+1] = "x"

            #print("e",eelmised)
            if laevapikkused:
                paiguta(n+1)
            else:
                valmis = True
        if valmis or kaua:
            break
    else:
        laevapikkused.append(pikkus)
        arvutil = deepcopy(eelmised[n])
        #print(911, len(laevapikkused))
    #print(saab)

#laevapikkused = [1,5,3,5,5,5,5,5,5]
laevapikkused = [1 for i in range(25)]
laevapikkused.sort()
print(laevapikkused)
f = dir1 + "/laud"
for i in laevapikkused:
    f += "-" + str(i)
f += ".txt"
print(f)
lauafail = open(f,"r")
arvutilauad = lauafail.read().split("\n"*2)
for i in range(len(arvutilauad)):
    arvutilauad[i] = arvutilauad[i].split("\n")
del arvutilauad[-1]
print("a",arvutilauad)
lauafail.close()
lauafail = open(f,"a")

eelmised = {i:[] for i in range(len(laevapikkused))}
print(eelmised)

arvutil = [[0 for i in range(10)] for j in range(10)]

algaeg = time()

paiguta(0)


for i in arvutil:
    print(i)
print()
for i in arvutil:
    for j in range(10):
        if i[j] == "x":
            i[j] = 0

arvutil1 = deepcopy(arvutil)
for i in arvutil1:
    for j in range(10):
        i[j] = str(i[j])
for i in arvutil1:
    print(i)

if kaua:
    arvutilh = choice(arvutilauad)
    print(arvutilh)
    arvutilh11 = [[j for j in i] for i in arvutilh]
    print(arvutilh11)
    arvutilv11 = []
    for i in range(10):
        arvutilv11.append([j[i] for j in arvutilh11])
    print(arvutilv11)
    j = randint(0,7)
    if j == 0:
        arvutil = arvutilh11
    elif j == 1:
        for i in range(10):
            arvutilh11[i] = arvutilh11[i][::-1]
        arvutil = arvutilh11
    elif j == 2:
        arvutil = arvutilh11[::-1]
    elif j == 3:
        for i in range(10):
            arvutilh11[i] = arvutilh11[i][::-1]
        arvutil = arvutilh11[::-1]
    elif j == 4:
        arvutil = arvutilv11
    elif j == 5:
        for i in range(10):
            arvutilv11[i] = arvutilv11[i][::-1]
        arvutil = arvutilv11
    elif j == 6:
        arvutil = arvutilv11[::-1]
    elif j == 7:
        for i in range(10):
            arvutilv11[i] = arvutilv11[i][::-1]
        arvutil = arvutilv11[::-1]
else:
    arvutilh11 = []
    arvutilv11 = []
    arvutilh12 = []
    arvutilv12 = []
    for i in range(10):
        arvutilh11.append("".join(arvutil1[i]))
        arvutilv11.append("".join([j[i] for j in arvutil1]))
        arvutilh12.append("".join(arvutil1[i])[::-1])
        arvutilv12.append("".join([j[i] for j in arvutil1])[::-1])
    arvutilh21 = arvutilh11[::-1]
    arvutilv21 = arvutilv11[::-1]
    arvutilh22 = arvutilh12[::-1]
    arvutilv22 = arvutilv12[::-1]
    if arvutilh11 not in arvutilauad and arvutilh21 not in arvutilauad and arvutilv11 not in arvutilauad and arvutilv21 not in arvutilauad and \
            arvutilh12 not in arvutilauad and arvutilh22 not in arvutilauad and arvutilv12 not in arvutilauad and arvutilv22 not in arvutilauad:
        for i in range(10):
            lauafail.write(arvutilh11[i]+"\n")
        lauafail.write("\n")
print()
for i in arvutil:
    for j in range(10):
        i[j] = int(i[j])
for i in arvutil:
    print(i)
print()
kaidud = []
laevad = []
for y in range(10):
    for x in range(10):
        if arvutil[y][x] == 1 and [x, y] not in kaidud:
            laev = [[x, y]]
            kaidud.append([x, y])
            a = 1
            while x + a <= 9:
                if arvutil[y][x + a] == 1:
                    laev.append([x + a, y])
                    kaidud.append([x + a, y])
                    a += 1
                else:
                    break
            a = 1
            while y + a <= 9:
                if arvutil[y + a][x] == 1:
                    laev.append([x, y + a])
                    kaidud.append([x, y + a])
                    a += 1
                else:
                    break
            laevad.append(laev)
#print(laevad)
laevapikkused1 = [len(i) for i in laevad]
print(laevapikkused1,len(laevapikkused1))
print(time()-algaeg)
