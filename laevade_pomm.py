# ------------------------------------------------
# kõik vajalikud impordid
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter.scrolledtext as tkst
import turtle
import base64
import os
from time import time
import pprint
from random import randint, choice
from copy import deepcopy
from classifier import NaiveBayesGuesser

# 1. -----------------------------------------------
# Veidrad funktsioonid ja vajalikud muutujad + classid
dir = "./playerdata"
try:
    os.listdir(dir)
except:
    os.mkdir(dir)

dir1 = "./boarddata"
try:
    os.listdir(dir1)
except:
    os.mkdir(dir1)

vot = "Laseme kõik laevad õhku"


class Laud:

    # laua initsialiseerimine
    def __init__(self):
        self.pikkus = 10
        self.laius = 10
        
        # list, mis hoiab valiklaud.laevad informatsiooni
        self.laevad = []
        # list, mis hoiab kaidud kohtade koordinaate
        self.kaidud = []
        self.laevapikkused = []
        self.laud = [[0 for i in range(self.pikkus)] for s in range(self.laius)]


        
# PrettyPrinteri deklaleerimine
pp = pprint.PrettyPrinter(indent=4)

# vajalikud lauad, peaks veel üle vaatama!
# valikute tegemise laud ehk
# mängija laud talle endale kuvatuna
valiklaud = Laud()
pp.pprint(valiklaud.laud)

# kolmas laud (l nagu laev)
# arvuti laevade informatsiooni
# ehk arvuti laud "talle kuvatuna"
arvutil = Laud()

# neljas laud (p nagu pomm)
# arvuti pommitamise informatsiooni
arvutip = Laud()

# viies laud (p nagu pomm)
# mängija pommitamise informatsioon ehk
# arvuti laud mängijale kuvatuna
mangijap = Laud()

def encode(string):
    return str(base64.b64encode(bytes(string, "utf-8")), "utf-8")

def decode(string):
    return str(base64.b64decode(bytes(string, "utf-8")), "utf-8")

# funkktsioon sisselogimise kontrollimiseks
def logi():
    global playerdata
    global kasu
    global sobib
    global kasutaja
    global login
    
    kasu = str(kasutaja.get())
    paro = str(parool.get())
    # print(kasu,paro)
    if "" in [kasu, paro]:
        mb.showerror("ERROR", "Kasutajanimi või parool on ebasobiv.")
    else:
        try:
            playerfile = open(dir + "/" + kasu + ".txt", "r", encoding="utf-8")
            a = decode(playerfile.readline())
            playerfile.close()
            if paro == a:
                sobib = True
                mb.showinfo("INFO", "Sisselogimine õnnestus.")
                login.destroy()
            else:
                mb.showerror("ERROR", "Sisestatud parool on vale.")
        except:
            mb.showerror("ERROR", "Kasutajat ei eksisteeri.")

# kasutajaloomise aken
def polekas():
    global kasutaja1
    global parool1
    global lookas
    lookas = Tk()
    lookas.title("Loo kasutaja")
    lookas.geometry('300x210')
    kas = Label(lookas, text="Kasutajanimi:")
    kas.place(x=75, y=10)
    kasutaja1 = Entry(lookas)
    kasutaja1.place(x=75, y=30, width=150)
    par = Label(lookas, text="Parool:")
    par.place(x=75, y=60)
    parool1 = Entry(lookas, show="*")
    parool1.place(x=75, y=80, width=150)
    nupp = ttk.Button(lookas, text="Loo kasutaja", command=lokas)
    nupp.place(x=75, y=110, width=150)

# funktsioon kontrollimaks, kas loodud kasutaja sobib
def lokas():
    global kasutaja1
    global parool1
    
    kasu = str(kasutaja1.get())
    paro = str(parool1.get())
    # print(kasu, paro)
    if "" in [kasu, paro]:
        mb.showerror("ERROR", "Kasutajanimi või parool on ebasobiv.")
    else:
        if kasu + ".txt" in os.listdir(dir):
            mb.showerror("ERROR", "Kasutajanimi on juba kasutuses, palun vali mõni teine.")
        else:
            playerfile = open(dir + "/" + kasu + ".txt", "w", encoding="utf-8")
            print(encode(paro) + "\n")
            playerfile.write(encode(paro) + "\n")
            playerfile.close()
            mb.showinfo("INFO", "Registreerimine õnnestus.")
            lookas.destroy()

# reeglite lugemisaken
def reeg():
    r = Toplevel(tervitus)
    r.title("Reeglid")
    reeglid = tkst.ScrolledText(master=r, wrap=WORD, width=50, height=20)
    reeglid.pack(padx=10, pady=10, fill=BOTH, expand=True)
    # Adding some text, to see if scroll is working as we expect it
    sis = open("Reeglid.txt", "r")
    reeglid.insert(INSERT, sis.read())
    sis.close()


def mang():
    global sobib
    global tervitus
    sobib = True
    tervitus.destroy()


# raskustaseme muutja
def rt(raskus):
    global rask
    global sobib
    global raskustase
    sobib = True
    raskustase = raskus
    # sulgeb raskustaseme valimisakna
    rask.destroy()

# 2. ------------------------------
# Siin asuvad kõik erinevate raskustasemete jaoks kasutatavad algoritmid

#
#
# Väga Lihtne
def veryeasy():
    return None

# 
# Suvaline laevade paigutus läbi tõenäosuste kasutades randinti
# Lihtne:
def easy(): 
    
    # n näitab paigutatud laevade summat
    def paiguta(n):
        global valmis
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
        eelmised[n] = deepcopy(arvutil.laud)
        print(eelmised)
        valmis = False
        while voim:
            arvutil.laud = deepcopy(eelmised[n])
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
            #for i in arvutil.laud:
                #print(i)
            saab = True
            if suund == 0:
                for i in range(pikkus):
                    if arvutil.laud[y][x+i] in [1,"x"]:
                        saab = False
                        break
            else:
                for i in range(pikkus):
                    if arvutil.laud[y+i][x] in [1,"x"]:
                        saab = False
                        break
            if saab:
                if suund == 0:
                    for i in range(pikkus):
                        arvutil.laud[y][x+i] = 1
                    if y > 0:
                        for i in range(pikkus):
                            if arvutil.laud[y-1][x+i] != 1:
                                arvutil.laud[y-1][x+i] = "x"
                    if y < 9:
                        for i in range(pikkus):
                            if arvutil.laud[y+1][x+i] != 1:
                                arvutil.laud[y+1][x+i] = "x"
                    if x > 0:
                        if arvutil.laud[y][x-1] != 1:
                            arvutil.laud[y][x-1] = "x"
                        if y > 0:
                            if arvutil.laud[y-1][x-1] != 1:
                                arvutil.laud[y-1][x-1] = "x"
                        if y < 9:
                            if arvutil.laud[y+1][x-1] != 1:
                                arvutil.laud[y+1][x-1] = "x"
                    if x + pikkus <= 9:
                        if arvutil.laud[y][x+pikkus] != 1:
                            arvutil.laud[y][x+pikkus] = "x"
                        if y > 0:
                            if arvutil.laud[y-1][x+pikkus] != 1:
                                arvutil.laud[y-1][x+pikkus] = "x"
                        if y < 9:
                            if arvutil.laud[y+1][x+pikkus] != 1:
                                arvutil.laud[y+1][x+pikkus] = "x"
                else:
                    for i in range(pikkus):
                        arvutil.laud[y+i][x] = 1
                    if x > 0:
                        for i in range(pikkus):
                            if arvutil.laud[y+i][x-1] != 1:
                                arvutil.laud[y+i][x-1] = "x"
                    if x < 9:
                        for i in range(pikkus):
                            if arvutil.laud[y+i][x+1] != 1:
                                arvutil.laud[y+i][x+1] = "x"
                    if y > 0:
                        if arvutil.laud[y-1][x] != 1:
                            arvutil.laud[y-1][x] = "x"
                        if x > 0:
                            if arvutil.laud[y-1][x-1] != 1:
                                arvutil.laud[y-1][x-1] = "x"
                        if x < 9:
                            if arvutil.laud[y-1][x+1] != 1:
                                arvutil.laud[y-1][x+1] = "x"
                    if y + pikkus <= 9:
                        if arvutil.laud[y+pikkus][x] != 1:
                            arvutil.laud[y+pikkus][x] = "x"
                        if x > 0:
                            if arvutil.laud[y+pikkus][x-1] != 1:
                                arvutil.laud[y+pikkus][x-1] = "x"
                        if x < 9:
                            if arvutil.laud[y+pikkus][x+1] != 1:
                                arvutil.laud[y+pikkus][x+1] = "x"

                #print("e",eelmised)
                if laevapikkused:
                    paiguta(n+1)
                else:
                    valmis = True
            if valmis or kaua:
                break
        else:
            laevapikkused.append(pikkus)
            arvutil.laud = deepcopy(eelmised[n])
            #print(911, len(laevapikkused))
        #print(saab)

    #laevapikkused = [1,5,3,5,5,5,5,5,5]
            
    # vaja teha muutujaks laevade arvu kohta
    mangijal
    laevapikkused = [5 for i in range(7)]
    laevapikkused.sort()
    print("laevapikkused:", laevapikkused)
    
    f = dir1 + "/laud"
    for i in laevapikkused:
        f += "-" + str(i)
    f += ".txt"
    print("mingi fail?: ", f)
    
    lauafail = open(f,"a")
    lauafail.close()
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

    arvutil.laud = [[0 for i in range(10)] for s in range(10)]

    algaeg = time()

    paiguta(0)


    for i in arvutil.laud:
        print(i)
    print()
    for i in arvutil.laud:
        for s in range(10):
            if i[s] == "x":
                i[s] = 0

    arvutil.laud1 = deepcopy(arvutil.laud)
    for i in arvutil.laud1:
        for s in range(10):
            i[s] = str(i[s])
    for i in arvutil.laud1:
        print(i)

    if kaua:
        arvutil.laudh = choice(arvutilauad)
        for i in range(10):
            arvutil.laudh[i] = decode(arvutil.laudh[i])
        print(arvutil.laudh)
        arvutil.laudh11 = [[s for s in i] for i in arvutil.laudh]
        print(arvutil.laudh11)
        arvutil.laudv11 = []
        for i in range(10):
            arvutil.laudv11.append([s[i] for s in arvutil.laudh11])
        print(arvutil.laudv11)
        s = randint(0,7)
        if s == 0:
            arvutil.laud = arvutil.laudh11
        elif s == 1:
            for i in range(10):
                arvutil.laudh11[i] = arvutil.laudh11[i][::-1]
            arvutil.laud = arvutil.laudh11
        elif s == 2:
            arvutil.laud = arvutil.laudh11[::-1]
        elif s == 3:
            for i in range(10):
                arvutil.laudh11[i] = arvutil.laudh11[i][::-1]
            arvutil.laud = arvutil.laudh11[::-1]
        elif s == 4:
            arvutil.laud = arvutil.laudv11
        elif s == 5:
            for i in range(10):
                arvutil.laudv11[i] = arvutil.laudv11[i][::-1]
            arvutil.laud = arvutil.laudv11
        elif s == 6:
            arvutil.laud = arvutil.laudv11[::-1]
        elif s == 7:
            for i in range(10):
                arvutil.laudv11[i] = arvutil.laudv11[i][::-1]
            arvutil.laud = arvutil.laudv11[::-1]
    else:
        arvutil.laudh11 = []
        arvutil.laudv11 = []
        arvutil.laudh12 = []
        arvutil.laudv12 = []
        for i in range(10):
            arvutil.laudh11.append("".join(arvutil.laud1[i]))
            arvutil.laudv11.append("".join([s[i] for s in arvutil.laud1]))
            arvutil.laudh12.append("".join(arvutil.laud1[i])[::-1])
            arvutil.laudv12.append("".join([s[i] for s in arvutil.laud1])[::-1])
        arvutil.laudh21 = arvutil.laudh11[::-1]
        arvutil.laudv21 = arvutil.laudv11[::-1]
        arvutil.laudh22 = arvutil.laudh12[::-1]
        arvutil.laudv22 = arvutil.laudv12[::-1]
        for i in range(10):
            arvutil.laudh11[i] = encode(arvutil.laudh11[i])
            arvutil.laudh12[i] = encode(arvutil.laudh12[i])
            arvutil.laudh21[i] = encode(arvutil.laudh21[i])
            arvutil.laudh22[i] = encode(arvutil.laudh22[i])
            arvutil.laudv11[i] = encode(arvutil.laudv11[i])
            arvutil.laudv12[i] = encode(arvutil.laudv12[i])
            arvutil.laudv21[i] = encode(arvutil.laudv21[i])
            arvutil.laudv22[i] = encode(arvutil.laudv22[i])
        print(arvutil.laudh11,"e")
        if arvutil.laudh11 not in arvutilauad and arvutil.laudh21 not in arvutilauad and arvutil.laudv11 not in arvutilauad and arvutil.laudv21 not in arvutilauad and \
                arvutil.laudh12 not in arvutilauad and arvutil.laudh22 not in arvutilauad and arvutil.laudv12 not in arvutilauad and arvutil.laudv22 not in arvutilauad:
            for i in range(10):
                lauafail.write(arvutil.laudh11[i]+"\n")
            lauafail.write("\n")
    print()
    lauafail.close()
    for i in arvutil.laud:
        for s in range(10):
            i[s] = int(i[s])
    for i in arvutil.laud:
        print(i)
    print()
    kaidud = []
    laevad = []
    for y in range(10):
        for x in range(10):
            if arvutil.laud[y][x] == 1 and [x, y] not in kaidud:
                laev = [[x, y]]
                kaidud.append([x, y])
                a = 1
                while x + a <= 9:
                    if arvutil.laud[y][x + a] == 1:
                        laev.append([x + a, y])
                        kaidud.append([x + a, y])
                        a += 1
                    else:
                        break
                a = 1
                while y + a <= 9:
                    if arvutil.laud[y + a][x] == 1:
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
    '''
    x = randint(0, 10) 
    y = randint(0, 10)
    while arvutip.laud[y][x] == 'O' or arvutip.laud[y][x] == 'x': 
        x = randint(0,9)
        y = randint(0,9)
    if mangijal.laud[y][x] == '@':
        arvutip.laud[y][x] = 'x'
    else:
        arvutip.laud[y][x] = 'O'
    '''
  
# Normal:
def normal():
    return None
#
# 
# Hard:
def hard():
    return None
    
#
#
# NaiveBayesGuesser algoritm
# Extreme:
def extreme():
    global arvutip
    nb = NaiveBayesGuesser(arvutip)
    n = 0
    while n != 4:
        print("guess:", nb.get_guess(arvutip.laud))
        n += 1

#
#
# nii-öelda "võimatu" raskustase, mis leiab üles mängija
# paigutatud laevad 
# Impossible:
def impossible():
  mangijal.laud[3][4] = '@'
  koord = [] #Leiab mängija laevad
  for i in range(mangijal.pikkus):
    if '@' in mangijal.laud[i]:
      indices = [j for j, x in enumerate(mangijal.laud[i]) if x == '@']
      for it in indices:
        koord.append([i,it])
  def impak():
    if koord != []:
      print(koord)
      arvutip.laud.laud[koord[0][0]][koord[0][1]] = 'x'
      koord.pop(0)
    
# 3. -----------------------------------------------
# Siin asuvad kõik laudadel liikumiseks/tulistamiseks jms vajalikud funktsioonid

# 3.1. ------------------------------------------------
# Siin asuvad kõik laevavalikus olevate nuppude funktsioonid

# laevavlikute nupu "N" funktsioon
def valik_ules():
    global j
    global lastpress
    global asukoht
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    print("valik asukoht:", asukoht)
    if asukoht[1] < 9:
        asukoht[1] += 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.goto(-248 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.penup()

# laevavalikute nupu "S" funktsioon
def valik_alla():
    global j
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    print("valik asukoht:", asukoht)
    if asukoht[1] > 0:
        asukoht[1] -= 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.goto(-248 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.penup()

# laevavalikute nupu "W" funktsioon
def valik_vasakule():
    global j
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    print("valik asukoht:", asukoht)
    if asukoht[0] > 0:
        asukoht[0] -= 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.goto(-248 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.penup()

# laevavalikute nupu "E" funktsioon
def valik_paremale():
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    print("valik asukoht:", asukoht)
    if asukoht[0] < 9:
        asukoht[0] += 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.goto(-248 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.penup()

# leavavalikute nupu "Paiguta" funktsioon
def valik_paiguta():
    global j
    global lastpress
    global asukoht
    if time() - lastpress < 0.6:
        return None
    lastpress = time() + 0.3
    x = asukoht[0]
    y = asukoht[1]
    if valiklaud.laud[y][x] == 0:
        valiklaud.laud[y][x] = 1
        j.goto(-225 + 50 * x, -225 + 50 * y)
        j.pencolor("#0000FF")
        j.pendown()
        j.dot(23)
        j.penup()
        for i in [[x + 1, y + 1], [x + 1, y - 1], [x - 1, y + 1], [x - 1, y - 1]]:
            if not (i[0] < 0 or i[1] < 0 or i[0] > 9 or i[1] > 9):
                if valiklaud.laud[i[1]][i[0]] == 0:
                    rist([i[0], i[1]])
                    valiklaud.laud[i[1]][i[0]] = "x"
        suund = 0
        if (x > 0 and valiklaud.laud[y][x - 1] == 1) or (x < 9 and valiklaud.laud[y][x + 1] == 1):
            suund = "h"
        elif (x == 0 and valiklaud.laud[y][x + 1] == 1) or (x == 9 and valiklaud.laud[y][x - 1] == 1):
            suund = "h"
        elif (y > 0 and valiklaud.laud[y - 1][x] == 1) or (y < 9 and valiklaud.laud[y + 1][x] == 1):
            suund = "v"
        elif (y == 0 and valiklaud.laud[y + 1][x] == 1) or (y == 9 and valiklaud.laud[y - 1][x] == 1):
            suund = "v"
        print(suund)
        if suund == "h":
            ots1 = x
            ots2 = x
            while ots1 > 0 and valiklaud.laud[y][ots1 - 1] == 1:
                ots1 -= 1
            while ots2 < 9 and valiklaud.laud[y][ots2 + 1] == 1:
                ots2 += 1
            print(ots1, ots2)
            a = 2
            juures1 = 0
            juures2 = 0
            while ots1 - a >= 0:
                try:
                    if valiklaud.laud[y][ots1 - a] == 1:
                        a += 1
                        juures1 += 1
                    else:
                        break
                except IndexError:
                    break
            a = 2
            while ots2 + a <= 9:
                try:
                    if valiklaud.laud[y][ots2 + a] == 1:
                        a += 1
                        juures2 += 1
                    else:
                        break
                except IndexError:
                    break

            l = ots2 - ots1 + 1
            print(l, juures1, juures2)
            if l + juures1 >= 5:
                if ots1 > 0:
                    if valiklaud.laud[y][ots1 - 1] == 0:
                        rist([ots1 - 1, y])
                        valiklaud.laud[y][ots1 - 1] = "x"
            if l + juures2 >= 5:
                if ots2 < 9:
                    if valiklaud.laud[y][ots2 + 1] == 0:
                        rist([ots2 + 1, y])
                        valiklaud.laud[y][ots2 + 1] = "x"
        elif suund == "v":
            ots1 = y
            ots2 = y
            while ots1 > 0 and valiklaud.laud[ots1 - 1][x] == 1:
                ots1 -= 1
            while ots2 < 9 and valiklaud.laud[ots2 + 1][x] == 1:
                ots2 += 1
            print(ots1, ots2)
            a = 2
            juures1 = 0
            juures2 = 0
            while ots1 - a >= 0:
                try:
                    if valiklaud.laud[ots1 - a][x] == 1:
                        a += 1
                        juures1 += 1
                    else:
                        break
                except IndexError:
                    break
            a = 2
            while ots2 + a <= 9:
                try:
                    if valiklaud.laud[ots2 + a][x] == 1:
                        a += 1
                        juures2 += 1
                    else:
                        break
                except IndexError:
                    break

            l = ots2 - ots1 + 1
            print(l, juures1, juures2)
            if l + juures1 >= 5:
                if ots1 > 0:
                    if valiklaud.laud[ots1 - 1][x] == 0:
                        rist([x, ots1 - 1])
                        valiklaud.laud[ots1 - 1][x] = "x"
            if l + juures2 >= 5:
                if ots2 < 9:
                    if valiklaud.laud[ots2 + 1][x] == 0:
                        rist([x, ots2 + 1])
                        valiklaud.laud[ots2 + 1][x] = "x"
        else:
            a = 2
            juures1 = 0
            juures2 = 0
            while x - a >= 0:
                try:
                    if valiklaud.laud[y][x - a] == 1:
                        a += 1
                        juures1 += 1
                    else:
                        break
                except IndexError:
                    break
            a = 2
            while x + a <= 9:
                try:
                    if valiklaud.laud[y][x + a] == 1:
                        a += 1
                        juures2 += 1
                    else:
                        break
                except IndexError:
                    break

            print(juures1, juures2)
            if juures1 >= 4:
                if x > 0:
                    if valiklaud.laud[y][x - 1] == 0:
                        rist([x - 1, y])
                        valiklaud.laud[y][x - 1] = "x"
            if juures2 >= 4:
                if x < 9:
                    if valiklaud.laud[y][x + 1] == 0:
                        rist([x + 1, y])
                        valiklaud.laud[y][x + 1] = "x"

            a = 2
            juures1 = 0
            juures2 = 0
            while y - a >= 0:
                try:
                    if valiklaud.laud[y - a][x] == 1:
                        a += 1
                        juures1 += 1
                    else:
                        break
                except IndexError:
                    break
            a = 2
            while y + a <= 9:
                try:
                    if valiklaud.laud[y + a][x] == 1:
                        a += 1
                        juures2 += 1
                    else:
                        break
                except IndexError:
                    break

            print(juures1, juures2)
            if juures1 >= 4:
                if y > 0:
                    if valiklaud.laud[y - 1][x] == 0:
                        rist([x, y - 1])
                        valiklaud.laud[y - 1][x] = "x"
            if juures2 >= 4:
                if y < 9:
                    if valiklaud.laud[y + 1][x] == 0:
                        rist([x, y + 1])
                        valiklaud.laud[y + 1][x] = "x"

        j.goto(-248 + 50 * x, -247 + 50 * y)

# laevavalikute laeva eemaldamisfunktsioon ehk nupu
# "Eemalda" funktsioon
def valik_eemalda():
    global j
    global asukoht
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time() + 0.3
    x = asukoht[0]
    y = asukoht[1]
    if valiklaud.laud[y][x] == 1:
        valiklaud.laud[y][x] = 0
        j.goto(-225 + 50 * x, -225 + 50 * y)
        j.pencolor("#FFFFFF")
        j.pendown()
        j.dot(23)
        j.penup()
        for i in [[x + 1, y + 1], [x + 1, y - 1], [x - 1, y + 1], [x - 1, y - 1]]:
            if not (i[0] < 0 or i[1] < 0 or i[0] > 9 or i[1] > 9):
                if valiklaud.laud[i[1]][i[0]] == "x":
                    lsd = []
                    if i[1] < 9:
                        if i[0] < 9:
                            lsd.append(valiklaud.laud[i[1] + 1][i[0] + 1])
                        if i[0] > 0:
                            lsd.append(valiklaud.laud[i[1] + 1][i[0] - 1])
                    if i[1] > 0:
                        if i[0] < 9:
                            lsd.append(valiklaud.laud[i[1] - 1][i[0] + 1])
                        if i[0] > 0:
                            lsd.append(valiklaud.laud[i[1] - 1][i[0] - 1])
                    if 1 not in lsd:
                        unrist([i[0], i[1]])
                        valiklaud.laud[i[1]][i[0]] = 0
                    del lsd

        ots1 = x
        while ots1 > 0 and valiklaud.laud[y][ots1 - 1] == 1:
            ots1 -= 1
        ots2 = y
        while ots2 > 0 and valiklaud.laud[ots2 - 1][x] == 1:
            ots2 -= 1
        ots3 = x
        while ots3 < 9 and valiklaud.laud[y][ots3 + 1] == 1:
            ots3 += 1
        ots4 = y
        while ots4 < 9 and valiklaud.laud[ots4 + 1][x] == 1:
            ots4 += 1
        print(ots1, ots2, ots3, ots4)

        if x - ots1 <= 4 and ots1 > 0:
            if valiklaud.laud[y][ots1 - 1] == "x":
                lsd = []
                if y < 9:
                    if ots1 - 1 < 9:
                        lsd.append(valiklaud.laud[y + 1][ots1])
                    if ots1 - 1 > 0:
                        lsd.append(valiklaud.laud[y + 1][ots1 - 2])
                if y > 0:
                    if ots1 - 1 < 9:
                        lsd.append(valiklaud.laud[y - 1][ots1])
                    if ots1 - 1 > 0:
                        lsd.append(valiklaud.laud[y - 1][ots1 - 2])
                if 1 not in lsd:
                    unrist([ots1 - 1, y])
                    valiklaud.laud[y][ots1 - 1] = 0
                del lsd
        if ots3 - x <= 4 and ots3 < 9:
            if valiklaud.laud[y][ots3 + 1] == "x":
                lsd = []
                if y < 9:
                    if ots3 + 1 < 9:
                        lsd.append(valiklaud.laud[y + 1][ots3 + 2])
                    if ots3 + 1 > 0:
                        lsd.append(valiklaud.laud[y + 1][ots3])
                if y > 0:
                    if ots3 + 1 < 9:
                        lsd.append(valiklaud.laud[y - 1][ots3 + 2])
                    if ots3 + 1 > 0:
                        lsd.append(valiklaud.laud[y - 1][ots3])
                if 1 not in lsd:
                    unrist([ots3 + 1, y])
                    valiklaud.laud[y][ots3 + 1] = 0
                del lsd
        if y - ots2 <= 4 and ots2 > 0:
            if valiklaud.laud[ots2 - 1][x] == "x":
                lsd = []
                if ots2 - 1 < 9:
                    if x < 9:
                        lsd.append(valiklaud.laud[ots2][x + 1])
                    if x > 0:
                        lsd.append(valiklaud.laud[ots2][x - 1])
                if ots2 - 1 > 0:
                    if x < 9:
                        lsd.append(valiklaud.laud[ots2 - 2][x + 1])
                    if x > 0:
                        lsd.append(valiklaud.laud[ots2 - 2][x - 1])
                if 1 not in lsd:
                    unrist([x, ots2 - 1])
                    valiklaud.laud[ots2 - 1][x] = 0
                del lsd
        if ots4 - y <= 4 and ots4 < 9:
            if valiklaud.laud[ots4 + 1][x] == "x":
                lsd = []
                if ots4 + 1 < 9:
                    if x < 9:
                        lsd.append(valiklaud.laud[ots4 + 2][x + 1])
                    if x > 0:
                        lsd.append(valiklaud.laud[ots4 + 2][x - 1])
                if ots4 + 1 > 0:
                    if x < 9:
                        lsd.append(valiklaud.laud[ots4][x + 1])
                    if x > 0:
                        lsd.append(valiklaud.laud[ots4][x - 1])
                if 1 not in lsd:
                    unrist([x, ots4 + 1])
                    valiklaud.laud[ots4 + 1][x] = 0
                del lsd

        j.goto(-248 + 50 * x, -247 + 50 * y)

# laevavalikute akna ristide eemaldamise funktsioon
def rist(asuk):
    global j
    global lastpress
    lastpress += 0.1
    j.pencolor("#FF0000")
    j.goto(-225 + 50 * asuk[0], -225 + 50 * asuk[1])
    j.pendown()
    j.left(45)
    j.forward(20)
    j.back(40)
    j.forward(20)
    j.right(90)
    j.forward(20)
    j.back(40)
    j.forward(20)
    j.left(45)
    j.penup()

# laevavalikute akna ristide märkimise funktsioon
def unrist(asuk):
    global j
    global lastpress
    lastpress += 0.1
    j.pencolor("#FFFFFF")
    j.goto(-225 + 50 * asuk[0], -225 + 50 * asuk[1])
    j.pendown()
    j.left(45)
    j.forward(20)
    j.back(40)
    j.forward(20)
    j.right(90)
    j.forward(20)
    j.back(40)
    j.forward(20)
    j.left(45)
    j.penup()

# funktsioon akna jaoks, mis küsib, kas kasutaja on kindel oma laevavalikutes
def valm1():
    if 1 in [i for e in valiklaud.laud for i in e]:
        global valm
        valm = Toplevel(control)
        valm.title("Oled sa kindel?")
        valm.geometry('300x80')

        msg = Label(valm, text="Oled sa kindel?")
        msg.place(x=100, y=5)
        nupp2 = ttk.Button(valm, text="JAH", command=valm2) # liigub edasi
        nupp2.place(x=75, y=40, width=75)
        nupp3 = ttk.Button(valm, text="EI", command=lambda: valm.destroy()) # liigub tagasi valimise juurde
        nupp3.place(x=150, y=40, width=75)
    else:
        mb.showerror("ERROR", "Laual ei ole ühtegi laeva.")

# kui valm1 ütleb, et mängija on kindel, siis valm2 laseb tal edasi liikuda
def valm2():
    global sobib
    global valm
    sobib = True
    valm.destroy()
    control.destroy()
    laevavalik.destroy()

# ründamisaknas kasutatava nupu "N" (ehk north) funktsioon
def atk_ules():
    global asukoht
    global kaik
    global j
    if not kaik:
        return None
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    print("rünnak asukoht:", asukoht)
    if asukoht[1] < 9:
        asukoht[1] += 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.penup()
# 3.2. ------------------------------------------------
# Siin asuvad ründamisaknas olevate nuppude funktsioonid

# ründamisaknas kasutatava nupu "S" (ehk south) funktsioon
def atk_alla():
    global asukoht
    global kaik
    global j
    if not kaik:
        return None
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    print("rünnak asukoht:", asukoht)
    if asukoht[1] > 0:
        asukoht[1] -= 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.penup()

# ründamisaknas kasutatava nupu "W" (ehk west) funktsioon
def atk_vasakule():
    global asukoht
    global kaik
    global j
    if not kaik:
        return None
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    print("rünnak asukoht:", asukoht)
    if asukoht[0] > 0:
        asukoht[0] -= 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.penup()

# ründamisaknas kasutatava nupu "E" (ehk east) funktsioon
def atk_paremale():
    global asukoht
    global kaik
    global j
    if not kaik:
        return None
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    print("rünnak asukoht:", asukoht)
    if asukoht[0] < 9:
        asukoht[0] += 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.penup()

# ründamisaknas kasutatava nupu "Märgista" funktsioon
def atk_mark():
    global asukoht
    global kaik
    global j
    if not kaik:
        return None
    global lastpress
    lastpress += 0.1
    j.pencolor("#A9A9A9")
    j.goto(125 + 50 * asukoht[0], -225 + 50 * asukoht[1])
    j.pendown()
    j.left(45)
    j.forward(10)
    j.back(20)
    j.forward(10)
    j.right(90)
    j.forward(10)
    j.back(20)
    j.forward(10)
    j.left(45)
    j.penup()
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    
    print("rünnak asukoht:", asukoht)

# ründamisaknas kasutatava nupu "Eemalda märgistus" funktsioon
def atk_unmark():
    global asukoht
    global kaik
    global j
    if not kaik:
        return None
    global lastpress
    lastpress += 0.1
    j.pencolor("#FFFFFF")
    j.goto(125 + 50 * asukoht[0], -225 + 50 * asukoht[1])
    j.pendown()
    j.left(45)
    j.forward(10)
    j.back(20)
    j.forward(10)
    j.right(90)
    j.forward(10)
    j.back(20)
    j.forward(10)
    j.left(45)
    j.penup()
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    
    print("rünnak asukoht:", asukoht)

# ründamisaknas kasutatava nupu "allahu akbar" funktsioon
def atk_pomm():
    global asukoht
    global kaik
    global j
    if not kaik:
        return None
    pass

    print("rünnak asukoht:", asukoht)
# 4. ----------------------------------
# Siin asub main mängu loop, mis jooksutab mängu
# ehk seob loogiliselt kokku kõik eelnevalt defineeritud
# funktsioonid ning loob vajalikud aknad.

def game_loop():
    global laevavalik
    global kasutaja
    global tervitus
    global asukoht
    global parool
    global sobib
    global login
    global rask

    # sisselogimisaken
    login = Tk()
    login.title("Login")
    login.geometry('300x210')

    loginmsg = Label(login, text="Mängimiseks pead sisse logima.")
    loginmsg.place(x=65, y=5)
    kas = Label(login, text="Kasutajanimi:")
    kas.place(x=75, y=40)
    kasutaja = Entry(login)
    kasutaja.place(x=75, y=60, width=150)
    par = Label(login, text="Parool:")
    par.place(x=75, y=90)
    parool = Entry(login, show="*")
    parool.place(x=75, y=110, width=150)
    nupp1 = ttk.Button(login, text="Logi sisse", command=logi)
    nupp1.place(x=75, y=140, width=150)
    nupp2 = ttk.Button(login, text="Mul pole veel kasutajat", command=polekas)
    nupp2.place(x=75, y=170, width=150)
    
    sobib = False
    login.mainloop()
    if not sobib:
        sys.exit()

    playerfile = open(dir + "/" + kasu + ".txt", "r", encoding="utf-8")

    # tervituse aken
    tervitus = Tk()
    tervitus.title("Tere tulemast, " + kasu)
    tervitus.geometry('300x110')
    msg = Label(tervitus, text="Mida soovid teha?")
    msg.place(x=100, y=5)
    nupp1 = ttk.Button(tervitus, text="Lugeda reegleid", command=reeg)
    nupp1.place(x=75, y=40, width=150)
    nupp2 = ttk.Button(tervitus, text="Mängida", command=mang)
    nupp2.place(x=75, y=70, width=150)
    
    sobib = False
    tervitus.mainloop()
    if not sobib:
        sys.exit()

    # raskustaseme aken
    rask = Tk()
    rask.title("Raskustase")
    rask.geometry('300x230')
    msg = Label(rask, text="Vali endale sobiv raskustase.")
    msg.place(x=73, y=5)
    nupp1 = ttk.Button(rask, text="Väga lihtne", command=lambda: rt(1))
    nupp1.place(x=75, y=40, width=150)
    nupp2 = ttk.Button(rask, text="Lihtne", command=lambda: rt(2))
    nupp2.place(x=75, y=70, width=150)
    nupp3 = ttk.Button(rask, text="Keskmine", command=lambda: rt(3))
    nupp3.place(x=75, y=100, width=150)
    nupp4 = ttk.Button(rask, text="Raske", command=lambda: rt(4))
    nupp4.place(x=75, y=130, width=150)
    nupp5 = ttk.Button(rask, text="Ekstreemne", command=lambda: rt(5))
    nupp5.place(x=75, y=160, width=150)
    nupp6 = ttk.Button(rask, text="Võimatu", command=lambda: rt(6))
    nupp6.place(x=75, y=190, width=150)
    
    sobib = False
    rask.mainloop()
    if not sobib:
        sys.exit()
    #print(raskustase)
    
    # laevavaliku aken
    laevavalik = Tk()
    laevavalik.title("laevade paigutamine")
    canvas = Canvas(master=laevavalik, width=700, height=700)
    canvas.pack()
    
    # rawturtle objekt
    global j
    j = turtle.RawTurtle(canvas)
    j.speed(0)
    j.hideturtle()
    j.pensize(10)
    j.penup()
    for i in range(11):
        j.goto(-250, -250 + 50 * i)
        j.pendown()
        j.forward(500)
        j.penup()
    j.left(90)
    for i in range(11):
        j.goto(-250 + 50 * i, -250)
        j.pendown()
        j.forward(500)
        j.penup()
    j.pensize(5)
    j.goto(-248, -247)
    asukoht = [0, 0]
    j.pencolor("#00FF00")
    j.pendown()
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.penup()
    
    global control
    control = Toplevel(laevavalik)
    control.title("Paigutaja kontrollimine")
    control.geometry('300x240')
    
    global lastpress
    lastpress = 0
    nupp1 = ttk.Button(control, text="N", command=valik_ules)
    nupp1.place(x=75, y=20, width=150)
    nupp2 = ttk.Button(control, text="W", command=valik_vasakule)
    nupp2.place(x=75, y=45, width=75)
    nupp3 = ttk.Button(control, text="E", command=valik_paremale)
    nupp3.place(x=150, y=45, width=75)
    nupp4 = ttk.Button(control, text="S", command=valik_alla)
    nupp4.place(x=75, y=70, width=150)
    nupp5 = ttk.Button(control, text="Paiguta", command=valik_paiguta)
    nupp5.place(x=75, y=120, width=150)
    nupp6 = ttk.Button(control, text="Eemalda", command=valik_eemalda)
    nupp6.place(x=75, y=145, width=150)
    nupp7 = ttk.Button(control, text="Valmis", command=valm1)
    nupp7.place(x=75, y=200, width=150)

    # jooksutab laevaed valiku loopi
    sobib = False
    global kaik
    kaik = True
    laevavalik.mainloop()
    if not sobib:
        sys.exit()

    # mangijal on mängija laud arvutile kuvatuna
    mangijal = valiklaud
    pp.pprint(valiklaud.laud)
    print()

    for i in mangijal.laud:
        for s in range(10):
            if i[s] == "x":
                i[s] = 0

    pp.pprint(mangijal.laud)
    print()
    pp.pprint(valiklaud.laud)

    for y in range(10):
        for x in range(10):
            if valiklaud.laud[y][x] == 1 and [x, y] not in valiklaud.kaidud:
                laev = [[x, y]]
                valiklaud.kaidud.append([x, y])
                a = 1
                while x + a <= 9:
                    if valiklaud.laud[y][x + a] == 1:
                        laev.append([x + a, y])
                        valiklaud.kaidud.append([x + a, y])
                        a += 1
                    else:
                        break
                a = 1
                while y + a <= 9:
                    if valiklaud.laud[y + a][x] == 1:
                        laev.append([x, y + a])
                        valiklaud.kaidud.append([x, y + a])
                        a += 1
                    else:
                        break
                valiklaud.laevad.append(laev)
    print(valiklaud.laevad)
    valiklaud.laevapikkused = [len(i) for i in valiklaud.laevad]
    print(valiklaud.laevapikkused)
    
    # lõplik mängulaud
    
    # valib raskustaseme vastavalt mängija algsele soovile
    if (raskustase == 1):
        veryeasy()
    elif (raskustase == 2):
        easy()
    elif (raskustase == 3):
        normal()
    elif (raskustase == 4):
        hard()
    elif (raskustase == 5):
        extreme()
    elif (raskustase == 6):
        impossible()

    laud = Tk()
    laud.title("laevade ründamine")
    canvas = Canvas(master=laud, width=1400, height=700)
    canvas.pack()

    j = turtle.RawTurtle(canvas)
    j.speed(0)
    j.hideturtle()
    j.pensize(10)
    j.penup()
    for i in range(11):
        j.goto(-600, -250 + 50 * i)
        j.pendown()
        j.forward(500)
        j.penup()
    j.left(90)
    for i in range(11):
        j.goto(-600 + 50 * i, -250)
        j.pendown()
        j.forward(500)
        j.penup()
    j.right(90)
    j.goto(-350, 270)
    j.write("SINU LAUD", True, "center", ("Arial", 40, "bold"))
    for i in range(11):
        j.goto(100, -250 + 50 * i)
        j.pendown()
        j.forward(500)
        j.penup()
    j.left(90)
    for i in range(11):
        j.goto(100 + 50 * i, -250)
        j.pendown()
        j.forward(500)
        j.penup()
    j.goto(350, 270)
    j.write("ARVUTI LAUD", False, "center", ("Arial", 40, "bold"))

    j.pencolor("#0000FF")
    j.pensize(23)
    for i in valiklaud.laevad:
        j.goto(-575 + 50 * i[0][0], -225 + 50 * i[0][1])
        j.pendown()
        for e in range(len(i)):
            j.goto(-575 + 50 * i[e][0], -225 + 50 * i[e][1])
        j.penup()

    j.pensize(5)
    j.goto(102, -247)
    asukoht = [0, 0]
    j.pencolor("#00FF00")
    j.pendown()
    for i in range(4):
        j.forward(45)
        j.right(90)
    j.penup()

    # pommitamise kontrollimise aken
    control = Toplevel(laud)
    control.title("Pommitaja kontrollimine")
    control.geometry('300x210')
    nupp1 = ttk.Button(control, text="N", command=atk_ules)
    nupp1.place(x=75, y=20, width=150)
    nupp2 = ttk.Button(control, text="W", command=atk_vasakule)
    nupp2.place(x=75, y=45, width=75)
    nupp3 = ttk.Button(control, text="E", command=atk_paremale)
    nupp3.place(x=150, y=45, width=75)
    nupp4 = ttk.Button(control, text="S", command=atk_alla)
    nupp4.place(x=75, y=70, width=150)
    nupp5 = ttk.Button(control, text="Märgista", command=atk_mark)
    nupp5.place(x=75, y=120, width=150)
    nupp6 = ttk.Button(control, text="Eemalda märgistus", command=atk_unmark)
    nupp6.place(x=75, y=145, width=150)
    nupp7 = ttk.Button(control, text="Allahu akbar!", command=atk_pomm)
    nupp7.place(x=75, y=170, width=150)
    
    laud.mainloop()

game_loop()
print()
print(encode("Hello World"))
a = base64.b64encode(bytes("Hello World", "utf-8"))
print(a)
b = base64.b64decode(a)
print(b)
print(str(b, "utf-8"))