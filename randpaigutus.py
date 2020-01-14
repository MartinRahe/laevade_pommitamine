from random import randint, choice
from copy import deepcopy
def paiguta(n):
    global valmis
    global arvutil
    pikkus = laevapikkused.pop()
    saab = False
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
        if valmis:
            break
    else:
        laevapikkused.append(pikkus)
        arvutil = deepcopy(eelmised[n])
        #print(911, len(laevapikkused))
    #print(saab)

laevapikkused = [1,5,3,5,5,5,5,5,5]
laevapikkused = [5 for i in range(7)]
laevapikkused.sort()
print(laevapikkused)

eelmised = {i:[] for i in range(len(laevapikkused))}
print(eelmised)

arvutil = [[0 for i in range(10)] for j in range(10)]

paiguta(0)

for i in arvutil:
    print(i)
    pass

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