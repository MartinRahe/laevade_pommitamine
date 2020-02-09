# ------------------------------------------------
# kõik vajalikud impordid
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter.scrolledtext as tkst
import turtle
from turtle import TurtleScreen
import base64
import os
from time import time, sleep
#import p#print
from random import randint, choice, random
from copy import deepcopy

# from classifier import NaiveBayesGuesser

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


# Pretty#printeri deklaleerimine
#pp = p#print.Pretty#printer(indent=4)

numtolet = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J"}
puudalla = ["No mida", "Kes siis nii teeb?", "Tundub tuttav?", "Suht kasutu"]
voidusonumid = ["Palju õnne, sa võitsid."]
kaotussonumid = ["Sel korral pidid arvutile alla vanduma."]

"""
# vajalikud lauad, peaks veel üle vaatama!
# valikute tegemise laud ehk
# mängija laud talle endale kuvatuna
valiklaud = Laud()
#pp.p#print(valiklaud.laud)
# kolmas laud (l nagu laev)
# arvuti laevade informatsiooni
# ehk arvuti laud "talle kuvatuna"
arvutil = Laud()
# neljas laud (p nagu pomm)
# arvuti pommitamise informatsiooni (arvuti ründab mängijat)
arvutip = Laud()
# viies laud (p nagu pomm)
# mängija pommitamise informatsioon ehk
# arvuti laud mängijale kuvatuna
mangijap = Laud()
"""


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
    # #print(kasu,paro)
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
    lookas.resizable(False, False)
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
    # #print(kasu, paro)
    if "" in [kasu, paro]:
        mb.showerror("ERROR", "Kasutajanimi või parool on ebasobiv.")
    else:
        if kasu + ".txt" in os.listdir(dir):
            mb.showerror("ERROR", "Kasutajanimi on juba kasutuses, palun vali mõni teine.")
        else:
            playerfile = open(dir + "/" + kasu + ".txt", "w", encoding="utf-8")
            #print(encode(paro) + "\n")
            playerfile.write(encode(paro) + "\n"*2)
            for i in range(10):
                playerfile.write(encode(10*"0 ") + "\n")
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
    reeglid.configure(state='disabled')


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

def find_index(mylist, item):
    for sub_list in mylist:
        if item in sub_list:
            return (mylist.index(sub_list), sub_list.index(item))
    return None

# 2. ------------------------------
# Siin asuvad kõik erinevate raskustasemete jaoks kasutatavad algoritmid

#
#
# Väga Lihtne
def veryeasy():
    easy()
    return None


def atk_veryeasy():
    global valiklaud
    global j
    global arvutitabamus
    # kas on -> joonista rist
    # kui ei ole -> joonista hall ring
    posx = randint(0, 9)
    posy = randint(0, 9)
    ajalug.insert(END, " " * 31 + numtolet[posx] + " " + str(posy))

    if valiklaud.laud[posy][posx] == 1:
        if arvutip.laud[posy][posx] == 0:
            # j.goto(125 + 50 * asukoht[0], -225 + 50 * asukoht[1])
            j.goto(-575 + (50 * posx), -225 + (50 * posy))
            j.pendown()
            j.pencolor("#FF0000")
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
            for laev in valiklaud.laevad:
                if [posx, posy] in laev:
                    laev.remove([posx, posy])
                    if laev:
                        ajalug.insert(END, "  Pihtas")
                    else:
                        ajalug.insert(END, "  Pihtas põhjas")
                    #print(valiklaud.laevad)
                    break
            arvutip.laud[posy][posx] = 4
            arvutitabamus += 1
        else:
            ajalug.insert(END, "  " + choice(puudalla))

    else:
        if arvutip.laud[posy][posx] == 0:
            # kui ei ole laeva
            j.pencolor("#A9A9A9")
            # j.goto(125 + 50 * asukoht[0], -225 + 50 * asukoht[1])
            j.goto(-575 + (50 * posx), -225 + (50 * posy))
            j.pendown()
            j.dot(15)
            j.penup()
            arvutip.laud[posy][posx] = 3
        else:
            ajalug.insert(END, "  " + choice(puudalla))

    j.penup()
    j.goto(102 + (50 * asukoht[0]), -247 + (50 * asukoht[1]))
    # mangijal vaja ka märkida

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
            voim = [[a, b, 1] for a in range(0, 11 - pikkus) for b in range(0, 10)]
        else:
            voim = [[a, b, c] for a in range(0, 11 - pikkus) for b in range(0, 10) for c in range(0, 2)]
        # #print(voim)
        eelmised[n] = deepcopy(arvutil.laud)
        #print(eelmised)
        valmis = False
        while voim:
            arvutil.laud = deepcopy(eelmised[n])
            valik = choice(voim)
            voim.remove(valik)
            # #print(voim)
            # #print(len(voim))
            alg1 = valik[0]
            alg2 = valik[1]
            suund = valik[2]
            if suund == 0:
                x, y = alg1, alg2
            else:
                x, y = alg2, alg1
            # #print(n)
            # #print(x,y,suund,pikkus)
            # for i in arvutil.laud:
            # #print(i)
            saab = True
            if suund == 0:
                for i in range(pikkus):
                    if arvutil.laud[y][x + i] in [1, "x"]:
                        saab = False
                        break
            else:
                for i in range(pikkus):
                    if arvutil.laud[y + i][x] in [1, "x"]:
                        saab = False
                        break
            if saab:
                if suund == 0:
                    for i in range(pikkus):
                        arvutil.laud[y][x + i] = 1
                    if y > 0:
                        for i in range(pikkus):
                            if arvutil.laud[y - 1][x + i] != 1:
                                arvutil.laud[y - 1][x + i] = "x"
                    if y < 9:
                        for i in range(pikkus):
                            if arvutil.laud[y + 1][x + i] != 1:
                                arvutil.laud[y + 1][x + i] = "x"
                    if x > 0:
                        if arvutil.laud[y][x - 1] != 1:
                            arvutil.laud[y][x - 1] = "x"
                        if y > 0:
                            if arvutil.laud[y - 1][x - 1] != 1:
                                arvutil.laud[y - 1][x - 1] = "x"
                        if y < 9:
                            if arvutil.laud[y + 1][x - 1] != 1:
                                arvutil.laud[y + 1][x - 1] = "x"
                    if x + pikkus <= 9:
                        if arvutil.laud[y][x + pikkus] != 1:
                            arvutil.laud[y][x + pikkus] = "x"
                        if y > 0:
                            if arvutil.laud[y - 1][x + pikkus] != 1:
                                arvutil.laud[y - 1][x + pikkus] = "x"
                        if y < 9:
                            if arvutil.laud[y + 1][x + pikkus] != 1:
                                arvutil.laud[y + 1][x + pikkus] = "x"
                else:
                    for i in range(pikkus):
                        arvutil.laud[y + i][x] = 1
                    if x > 0:
                        for i in range(pikkus):
                            if arvutil.laud[y + i][x - 1] != 1:
                                arvutil.laud[y + i][x - 1] = "x"
                    if x < 9:
                        for i in range(pikkus):
                            if arvutil.laud[y + i][x + 1] != 1:
                                arvutil.laud[y + i][x + 1] = "x"
                    if y > 0:
                        if arvutil.laud[y - 1][x] != 1:
                            arvutil.laud[y - 1][x] = "x"
                        if x > 0:
                            if arvutil.laud[y - 1][x - 1] != 1:
                                arvutil.laud[y - 1][x - 1] = "x"
                        if x < 9:
                            if arvutil.laud[y - 1][x + 1] != 1:
                                arvutil.laud[y - 1][x + 1] = "x"
                    if y + pikkus <= 9:
                        if arvutil.laud[y + pikkus][x] != 1:
                            arvutil.laud[y + pikkus][x] = "x"
                        if x > 0:
                            if arvutil.laud[y + pikkus][x - 1] != 1:
                                arvutil.laud[y + pikkus][x - 1] = "x"
                        if x < 9:
                            if arvutil.laud[y + pikkus][x + 1] != 1:
                                arvutil.laud[y + pikkus][x + 1] = "x"

                # #print("e",eelmised)
                if laevapikkused:
                    paiguta(n + 1)
                else:
                    valmis = True
            if valmis or kaua:
                break
        else:
            laevapikkused.append(pikkus)
            arvutil.laud = deepcopy(eelmised[n])
            # #print(911, len(laevapikkused))
        # #print(saab)

    # laevapikkused = [1,5,3,5,5,5,5,5,5]
    # vaja teha muutujaks laevade arvu kohta
    laevapikkused = valiklaud.laevapikkused
    laevapikkused.sort()
    #print("laevapikkused:", laevapikkused)

    f = dir1 + "/laud"
    for i in laevapikkused:
        f += "-" + str(i)
    f += ".txt"
    #print("mingi fail?: ", f)

    lauafail = open(f, "a")
    lauafail.close()
    lauafail = open(f, "r")
    arvutilauad = lauafail.read().split("\n" * 2)
    for i in range(len(arvutilauad)):
        arvutilauad[i] = arvutilauad[i].split("\n")
    del arvutilauad[-1]
    #print("a", arvutilauad)
    lauafail.close()
    lauafail = open(f, "a")

    eelmised = {i: [] for i in range(len(laevapikkused))}
    #print(eelmised)

    arvutil.laud = [[0 for i in range(10)] for s in range(10)]

    algaeg = time()

    paiguta(0)

    for i in arvutil.laud:
        #print(i)
        pass
    #print()
    for i in arvutil.laud:
        for s in range(10):
            if i[s] == "x":
                i[s] = 0

    arvutil.laud1 = deepcopy(arvutil.laud)
    for i in arvutil.laud1:
        for s in range(10):
            i[s] = str(i[s])
    for i in arvutil.laud1:
        #print(i)
        pass

    if kaua:
        arvutil.laudh = choice(arvutilauad)
        for i in range(10):
            arvutil.laudh[i] = decode(arvutil.laudh[i])
        #print(arvutil.laudh)
        arvutil.laudh11 = [[s for s in i] for i in arvutil.laudh]
        #print(arvutil.laudh11)
        arvutil.laudv11 = []
        for i in range(10):
            arvutil.laudv11.append([s[i] for s in arvutil.laudh11])
        #print(arvutil.laudv11)
        s = randint(0, 7)
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
        #print(arvutil.laudh11, "e")
        if arvutil.laudh11 not in arvutilauad and arvutil.laudh21 not in arvutilauad and arvutil.laudv11 not in arvutilauad and arvutil.laudv21 not in arvutilauad and \
                arvutil.laudh12 not in arvutilauad and arvutil.laudh22 not in arvutilauad and arvutil.laudv12 not in arvutilauad and arvutil.laudv22 not in arvutilauad:
            for i in range(10):
                lauafail.write(arvutil.laudh11[i] + "\n")
            lauafail.write("\n")
    #print()
    lauafail.close()
    for i in arvutil.laud:
        for s in range(10):
            i[s] = int(i[s])
    for i in arvutil.laud:
        #print(i)
        pass
    #print()
    kaidud = []
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
                arvutil.laevad.append(laev)

    #print(arvutil.laevad)
    arvutil.laevapikkused = [len(i) for i in arvutil.laevad]
    #print(arvutil.laevapikkused, len(arvutil.laevapikkused))
    #print(time() - algaeg)

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


def atk_easy():
    global ajalug
    global arvutitabamus
    global leitud
    global hml_save
    # muidu proovi leida üles kogu laev
    # ei tulista samasse kohta
    # märgistab võimatud ruudud

    # arvutip - arvuti ründab mängijat
    # valiklaud - mängija laevade info

    # 0 - teadmata
    # 2 - märgendus
    # 3 - mööda
    # 4 - tabamus
    # 5 - uuritud tabamus

    if (leitud):
        #print("leitud ",leitud)

        tabamus = False
        while not tabamus:
            alg = choice(leitud)
            #print(alg)
            posx = alg[0]
            posy = alg[1]
            tabatud = False
            moves = [[0, 1], [1, 0], [-1, 0], [0, -1]]
            while not tabatud:

                kaik = choice(moves)
                moves.remove(kaik)
                if posx + kaik[1] >= 0 and posy + kaik[0] >= 0 and posx + kaik[1] <= 9 and posy + kaik[0] <= 9:
                    if arvutip.laud[posy + kaik[0]][posx + kaik[1]] == 0:
                        posx += kaik[1]
                        posy += kaik[0]
                        ajalug.insert(END, " " * 31 + numtolet[posx] + " " + str(posy))
                        if valiklaud.laud[posy][posx] == 1:
                            leitud.append([posx,posy])
                            arvutitabamus += 1
                            hml_save[posx][posy] += 1
                            arvutip.laud[posy][posx] = 4
                            for laev in valiklaud.laevad:
                                if [posx, posy] in laev:
                                    laev.remove([posx, posy])
                                    if laev:
                                        ajalug.insert(END, "  Pihtas")
                                    else:
                                        ajalug.insert(END, "  Pihtas põhjas")
                                        leitud = []
                                        if kaik[0] == 0:
                                            a = posx
                                            while a >= 0:
                                                if arvutip.laud[posy][a] == 4:
                                                    a -= 1
                                                else:
                                                    if arvutip.laud[posy][a] == 0:
                                                        arvutip.laud[posy][a] = 2
                                                        j.penup()
                                                        j.goto(-575 + (50 * a),-225 + (50 * posy))
                                                        j.pencolor("#A9A9A9")
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
                                                    break
                                            a = posx
                                            while a <= 9:
                                                if arvutip.laud[posy][a] == 4:
                                                    a += 1
                                                else:
                                                    if arvutip.laud[posy][a] == 0:
                                                        arvutip.laud[posy][a] = 2
                                                        j.penup()
                                                        j.goto(-575 + (50 * a), -225 + (50 * posy))
                                                        j.pencolor("#A9A9A9")
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
                                                    break

                                        else:
                                            a = posy
                                            while a >= 0:
                                                if arvutip.laud[a][posx] == 4:
                                                    a -= 1
                                                else:
                                                    if arvutip.laud[a][posx] == 0:
                                                        arvutip.laud[a][posx] = 2
                                                        j.penup()
                                                        j.goto(-575 + (50 * posx),-225 + (50 * a))
                                                        j.pencolor("#A9A9A9")
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
                                                    break
                                            a = posy
                                            while a <= 9:
                                                if arvutip.laud[a][posx] == 4:
                                                    a += 1
                                                else:
                                                    if arvutip.laud[a][posx] == 0:
                                                        arvutip.laud[a][posx] = 2
                                                        j.penup()
                                                        j.goto(-575 + (50 * posx), -225 + (50 * a))
                                                        j.pencolor("#A9A9A9")
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
                                                    break

                            j.penup()
                            j.goto(-575 + (50 * posx), -225 + (50 * posy))
                            j.pendown()
                            j.pencolor("#FF0000")
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

                            pos = [[1, 1], [-1, -1], [-1, 1], [1, -1]]

                            for item in pos:
                                if posx + item[0] >= 0 and posy + item[1] >= 0 and posx + item[0] <= 9 and posy + item[1] <= 9:
                                    if arvutip.laud[posy + item[1]][posx + item[0]] == 0:
                                        arvutip.laud[posy + item[1]][posx + item[0]] = 2

                                        j.penup()
                                        j.goto(-575 + (50 * (posx + item[0])), -225 + (50 * (posy + item[1])))
                                        j.pencolor("#A9A9A9")
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

                        else:
                            j.penup()
                            j.pencolor("#A9A9A9")
                            j.goto(-575 + (50 * posx), -225 + (50 * posy))
                            j.pendown()
                            j.dot(15)
                            j.penup()
                            arvutip.laud[posy][posx] = 3
                        tabatud = True
                        tabamus = True
                        break

                if not moves:
                    leitud.remove(alg)
                    break


    # kui laud on tühi või kõik laevad on põhjas siis tulista suvaliselt
    else:

        # kontrollib, et ei tulista võimatutesse kohtadesse.
        lask = False
        while not lask:

            posx = randint(0, 9)
            posy = randint(0, 9)

            if arvutip.laud[posy][posx] == 0:

                lask = True
                ajalug.insert(END, " " * 31 + numtolet[posx] + " " + str(posy))

                if valiklaud.laud[posy][posx] == 1:

                    # kui on laev ehk tabamus
                    leitud.append([posx, posy])
                    for laev in valiklaud.laevad:
                        if [posx, posy] in laev:
                            laev.remove([posx, posy])
                            arvutip.laud[posy][posx] = 4
                            if laev:
                                ajalug.insert(END, "  Pihtas")
                            else:
                                ajalug.insert(END, "  Pihtas põhjas")
                                leitud = []
                                moves = [[0, 1], [1, 0], [-1, 0], [0, -1]]

                                for move in moves:

                                    if posx + move[1] >= 0 and posy + move[0] >= 0 and posx + move[1] <= 9 and posy + move[0] <= 9:
                                        if arvutip.laud[posy + move[0]][posx + move[1]] == 0:
                                            j.penup()
                                            j.goto(-575 + (50 * (posx + move[1])), -225 + (50 * (posy + move[0])))
                                            j.pencolor("#A9A9A9")
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

                                            arvutip.laud[posy + move[0]][posx + move[1]] = 2

                            #print(valiklaud.laevad)
                            break

                    arvutip.laud[posy][posx] = 4
                    hml_save[posx][posy] += 1
                    arvutitabamus += 1


                    j.penup()
                    j.goto(-575 + (50 * posx), -225 + (50 * posy))
                    j.pendown()
                    j.pencolor("#FF0000")
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

                    # kui pihta, siis tuleb teha ka märgistused

                    # märgistused, kui laseb pihta
                    pos = [[1, 1], [-1, -1], [-1, 1], [1, -1]]

                    for item in pos:
                        #print(posx + item[0],posy + item[1])
                        if posx + item[0] >= 0 and posy + item[1] >= 0 and posx + item[0] <= 9 and posy + item[1] <= 9:
                            if arvutip.laud[posy + item[1]][posx + item[0]] == 0:
                                arvutip.laud[posy + item[1]][posx + item[0]] = 2

                                j.penup()
                                j.goto(-575 + (50 * (posx + item[0])), -225 + (50 * (posy + item[1])))
                                j.pencolor("#A9A9A9")
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

                else:
                    # kui ei ole laeva ehk mööda
                    j.penup()
                    j.pencolor("#A9A9A9")
                    j.goto(-575 + (50 * posx), -225 + (50 * posy))
                    j.pendown()
                    j.dot(15)
                    j.penup()

                    arvutip.laud[posy][posx] = 3


        #print("arvutip")
        #pp.p#print(arvutip.laud)
        return None

    return None


# Normal:
def normal():
    easy()

# diagonaalid + atk_easy
def atk_normal():
    global leitud
    global ajalug
    global hml_save
    global diagonaalid
    global arvutitabamus

    #pp.p#print(diagonaalid)

    if (leitud):
        atk_easy()
    else:

        tulistas = False
        while not tulistas:

            lask = choice(choice(diagonaalid))
            #print("lask:", lask)

            posy = lask[0]
            posx = lask[1]
            for pos in diagonaalid:
                if [posy, posx] in pos:
                    pos.remove([posy, posx])

            for pos in diagonaalid:
                if pos == []:
                    diagonaalid.remove(pos)

            if arvutip.laud[posy][posx] == 0:

                tulistas = True
                ajalug.insert(END, " " * 31 + numtolet[posx] + " " + str(posy))

                if valiklaud.laud[posy][posx] == 1:

                    # kui on laev ehk tabamus
                    leitud.append([posx, posy])
                    for laev in valiklaud.laevad:
                        if [posx, posy] in laev:
                            laev.remove([posx, posy])
                            arvutip.laud[posy][posx] = 4
                            if laev:
                                ajalug.insert(END, "  Pihtas")
                            else:
                                ajalug.insert(END, "  Pihtas põhjas")
                                leitud = []
                                moves = [[0, 1], [1, 0], [-1, 0], [0, -1]]

                                for move in moves:

                                    if posx + move[1] >= 0 and posy + move[0] >= 0 and posx + move[1] <= 9 and posy + \
                                            move[0] <= 9:
                                        if arvutip.laud[posy + move[0]][posx + move[1]] == 0:
                                            j.penup()
                                            j.goto(-575 + (50 * (posx + move[1])), -225 + (50 * (posy + move[0])))
                                            j.pencolor("#A9A9A9")
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

                                            arvutip.laud[posy + move[0]][posx + move[1]] = 2

                            #print(valiklaud.laevad)
                            break

                    arvutip.laud[posy][posx] = 4
                    hml_save[posx][posy] += 1
                    arvutitabamus += 1

                    j.penup()
                    j.goto(-575 + (50 * posx), -225 + (50 * posy))
                    j.pendown()
                    j.pencolor("#FF0000")
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

                    # kui pihta, siis tuleb teha ka märgistused

                    # märgistused, kui laseb pihta
                    pos = [[1, 1], [-1, -1], [-1, 1], [1, -1]]

                    for item in pos:
                        #print(posx + item[0], posy + item[1])
                        if posx + item[0] >= 0 and posy + item[1] >= 0 and posx + item[0] <= 9 and posy + item[1] <= 9:
                            if arvutip.laud[posy + item[1]][posx + item[0]] == 0:
                                arvutip.laud[posy + item[1]][posx + item[0]] = 2

                                j.penup()
                                j.goto(-575 + (50 * (posx + item[0])), -225 + (50 * (posy + item[1])))
                                j.pencolor("#A9A9A9")
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

                else:
                    # kui ei ole laeva ehk mööda
                    j.penup()
                    j.pencolor("#A9A9A9")
                    j.goto(-575 + (50 * posx), -225 + (50 * posy))
                    j.pendown()
                    j.dot(15)
                    j.penup()

                    arvutip.laud[posy][posx] = 3

    return None


#
#
# Hard:
def hard():
    easy()

# HeatMap
def atk_hard():
    global hml
    global leitud
    global ajalug
    global hml_save
    global arvutitabamus

    # hml - kasutab tulistamiseks
    # hml_save - salvestab heatmapi

    #print("hml:")
    #pp.p#print(hml)
    #print("hmlmax:", max(max(hml)))

    if (leitud):
        atk_easy()
    elif max(max(hml)) != 0:

        while max(max(hml)) != 0:

            tuli = find_index(hml, max(max(hml)))
            posy = tuli[1]
            posx = tuli[0]
            #pp.p#print(hml)
            #print(tuli)
            #print(max(max(hml)))

            if arvutip.laud[posy][posx] == 0:

                lask = True
                ajalug.insert(END, " " * 31 + numtolet[posx] + " " + str(posy))

                if valiklaud.laud[posy][posx] == 1:

                    # kui on laev ehk tabamus
                    leitud.append([posx, posy])
                    for laev in valiklaud.laevad:
                        if [posx, posy] in laev:

                            laev.remove([posx, posy])
                            arvutip.laud[posy][posx] = 4

                            if laev:
                                ajalug.insert(END, "  Pihtas")
                            else:
                                ajalug.insert(END, "  Pihtas põhjas")
                                leitud = []
                                moves = [[0, 1], [1, 0], [-1, 0], [0, -1]]

                                for move in moves:

                                    if posx + move[1] >= 0 and posy + move[0] >= 0 and posx + move[1] <= 9 and posy + \
                                            move[0] <= 9:
                                        if arvutip.laud[posy + move[0]][posx + move[1]] == 0:
                                            j.penup()
                                            j.goto(-575 + (50 * (posx + move[1])), -225 + (50 * (posy + move[0])))
                                            j.pencolor("#A9A9A9")
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

                                            arvutip.laud[posy + move[0]][posx + move[1]] = 2
                            #print(valiklaud.laevad)
                            break
                    arvutip.laud[posy][posx] = 4
                    hml_save[posx][posy] += 1
                    hml[posy][posx] = 0
                    arvutitabamus += 1

                    j.penup()
                    j.goto(-575 + (50 * posx), -225 + (50 * posy))
                    j.pendown()
                    j.pencolor("#FF0000")
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

                    # kui pihta, siis tuleb teha ka märgistused

                    # märgistused, kui laseb pihta
                    pos = [[1, 1], [-1, -1], [-1, 1], [1, -1]]

                    for item in pos:
                        #print(posx + item[0], posy + item[1])
                        if posx + item[0] >= 0 and posy + item[1] >= 0 and posx + item[0] <= 9 and posy + item[1] <= 9:
                            if arvutip.laud[posy + item[1]][posx + item[0]] == 0:
                                arvutip.laud[posy + item[1]][posx + item[0]] = 2
                                hml[posy + item[1]][posx + item[0]] = 0

                                j.penup()
                                j.goto(-575 + (50 * (posx + item[0])), -225 + (50 * (posy + item[1])))
                                j.pencolor("#A9A9A9")
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


                    return None

                else:
                    # kui ei ole laeva ehk mööda
                    j.penup()
                    j.pencolor("#A9A9A9")
                    j.goto(-575 + (50 * posx), -225 + (50 * posy))
                    j.pendown()
                    j.dot(15)
                    j.penup()

                    arvutip.laud[posy][posx] = 3
                    hml[posy][posx] = 0
                    return None

            # kui visuaal ütleb, et ei ole laeva
            else:
                #print("reached")
                hml[posx][posy] = 0
        else:
            atk_easy()
            return None
    else:
        atk_easy()
        return None

    return None

def extreme():
    easy()

# Probability Density function
def atk_extreme():
    atk_hard()


#
#
# nii-öelda "võimatu" raskustase, mis leiab üles mängija
# paigutatud laevad
# Impossible:
def impossible():
    easy()


def atk_impossible():
    global hml
    global leitud
    global ajalug
    global hml_save
    global arvutitabamus
    global mangijatabamus
    if (leitud):
        atk_easy()
    elif arvutitabamus - mangijatabamus >= 3:
        atk_extreme()
    else:
        lastavlaev = []
        while not lastavlaev:
            lastavlaev = choice(valiklaud.laevad)
        lask = choice(lastavlaev)
        posx = lask[0]
        posy = lask[1]
        ajalug.insert(END, " " * 31 + numtolet[posx] + " " + str(posy))

        if valiklaud.laud[posy][posx] == 1:

            # kui on laev ehk tabamus
            leitud.append([posx, posy])
            for laev in valiklaud.laevad:
                if [posx, posy] in laev:
                    laev.remove([posx, posy])
                    arvutip.laud[posy][posx] = 4
                    if laev:
                        ajalug.insert(END, "  Pihtas")
                    else:
                        ajalug.insert(END, "  Pihtas põhjas")
                        leitud = []
                        moves = [[0, 1], [1, 0], [-1, 0], [0, -1]]

                        for move in moves:

                            if posx + move[1] >= 0 and posy + move[0] >= 0 and posx + move[1] <= 9 and posy + move[
                                0] <= 9:
                                if arvutip.laud[posy + move[0]][posx + move[1]] == 0:
                                    j.penup()
                                    j.goto(-575 + (50 * (posx + move[1])), -225 + (50 * (posy + move[0])))
                                    j.pencolor("#A9A9A9")
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

                                    arvutip.laud[posy + move[0]][posx + move[1]] = 2

                    #print(valiklaud.laevad)
                    break

            arvutip.laud[posy][posx] = 4
            hml_save[posx][posy] += 1
            arvutitabamus += 1

            j.penup()
            j.goto(-575 + (50 * posx), -225 + (50 * posy))
            j.pendown()
            j.pencolor("#FF0000")
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

            # kui pihta, siis tuleb teha ka märgistused

            # märgistused, kui laseb pihta
            pos = [[1, 1], [-1, -1], [-1, 1], [1, -1]]

            for item in pos:
                #print(posx + item[0], posy + item[1])
                if posx + item[0] >= 0 and posy + item[1] >= 0 and posx + item[0] <= 9 and posy + item[1] <= 9:
                    if arvutip.laud[posy + item[1]][posx + item[0]] == 0:
                        arvutip.laud[posy + item[1]][posx + item[0]] = 2

                        j.penup()
                        j.goto(-575 + (50 * (posx + item[0])), -225 + (50 * (posy + item[1])))
                        j.pencolor("#A9A9A9")
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

        else:
            # kui ei ole laeva ehk mööda
            j.penup()
            j.pencolor("#A9A9A9")
            j.goto(-575 + (50 * posx), -225 + (50 * posy))
            j.pendown()
            j.dot(15)
            j.penup()

            arvutip.laud[posy][posx] = 3



# 3. -----------------------------------------------
# Siin asuvad kõik laudadel liikumiseks/tulistamiseks jms vajalikud funktsioonid

# 3.1. ------------------------------------------------
# Siin asuvad kõik laevavalikus olevate nuppude funktsioonid

# laevavlikute nupu "N" funktsioon
def valik_ules():
    global j
    global lastpress
    global asukoht
    if time() - lastpress < 0.05: #0.6
        return None
    lastpress = time()
    j.pendown()
    #print("valik asukoht:", asukoht)
    if asukoht[1] < 9:
        asukoht[1] += 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    j.goto(-248 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pendown()
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()


# laevavalikute nupu "S" funktsioon
def valik_alla():
    global j
    global lastpress
    if time() - lastpress < 0.05: #0.6
        return None
    lastpress = time()
    j.pendown()
    #print("valik asukoht:", asukoht)
    if asukoht[1] > 0:
        asukoht[1] -= 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    j.goto(-248 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pendown()
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()


# laevavalikute nupu "W" funktsioon
def valik_vasakule():
    global j
    global lastpress
    if time() - lastpress < 0.05: #0.6
        return None
    lastpress = time()
    j.pendown()
    #print("valik asukoht:", asukoht)
    if asukoht[0] > 0:
        asukoht[0] -= 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    j.goto(-248 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pendown()
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()


# laevavalikute nupu "E" funktsioon
def valik_paremale():
    global lastpress
    if time() - lastpress < 0.05: #0.6
        return None
    lastpress = time()
    j.pendown()
    #print("valik asukoht:", asukoht)
    if asukoht[0] < 9:
        asukoht[0] += 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    j.goto(-248 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pendown()
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()


# leavavalikute nupu "Paiguta" funktsioon
def valik_paiguta():
    global j
    global lastpress
    global asukoht
    if time() - lastpress < 0.05: #0.6
        return None
    lastpress = time() #+ 0.3
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
        #print(suund)
        if suund == "h":
            ots1 = x
            ots2 = x
            while ots1 > 0 and valiklaud.laud[y][ots1 - 1] == 1:
                ots1 -= 1
            while ots2 < 9 and valiklaud.laud[y][ots2 + 1] == 1:
                ots2 += 1
            #print(ots1, ots2)
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
            #print(l, juures1, juures2)
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
            #print(ots1, ots2)
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
            #print(l, juures1, juures2)
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

            #print(juures1, juures2)
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

            #print(juures1, juures2)
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
    if time() - lastpress < 0.05: #0.6
        return None
    lastpress = time() #+ 0.3
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
        #print(ots1, ots2, ots3, ots4)

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
    #lastpress += 0.1
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
    #lastpress += 0.1
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
        nupp2 = ttk.Button(valm, text="JAH", command=valm2)  # liigub edasi
        nupp2.place(x=75, y=40, width=75)
        nupp3 = ttk.Button(valm, text="EI", command=lambda: valm.destroy())  # liigub tagasi valimise juurde
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
    if time() - lastpress < 0.05: #0.6
        return None
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    lastpress = time()
    if asukoht[1] < 9:
        asukoht[1] += 1
    else:
        return None
    j.pendown()
    j.pencolor("#000000")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pendown()
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    #print("rünnak asukoht:", asukoht)


# 3.2. ------------------------------------------------
# Siin asuvad ründamisaknas olevate nuppude funktsioonid

# tingimuslause if not kaik kontrollib, kas oli mängija kord rünnata.
# On vajalik siis, kui implementeerida arvutile mingi "mõltemisaeg"

# ründamisaknas kasutatava nupu "S" (ehk south) funktsioon
def atk_alla():
    global asukoht
    global kaik
    global j

    if not kaik:
        return None

    global lastpress
    if time() - lastpress < 0.05: #0.6
        return None
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    lastpress = time()
    if asukoht[1] > 0:
        asukoht[1] -= 1
    else:
        return None
    j.pendown()
    j.pencolor("#000000")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pendown()
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    #print("rünnak asukoht:", asukoht)


# ründamisaknas kasutatava nupu "W" (ehk west) funktsioon
def atk_vasakule():
    global asukoht
    global kaik
    global j

    if not kaik:
        return None

    global lastpress
    if time() - lastpress < 0.05: #0.6
        return None
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    lastpress = time()
    if asukoht[0] > 0:
        asukoht[0] -= 1
    else:
        return None
    j.pendown()
    j.pencolor("#000000")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pendown()
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    #print("rünnak asukoht:", asukoht)


# ründamisaknas kasutatava nupu "E" (ehk east) funktsioon
def atk_paremale():
    global asukoht
    global kaik
    global j

    if not kaik:
        return None

    global lastpress
    if time() - lastpress < 0.05: #0.6
        return None
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    lastpress = time()
    j.pendown()
    if asukoht[0] < 9:
        asukoht[0] += 1
    else:
        return None
    j.pencolor("#000000")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    j.pendown()
    j.pencolor("#00FF00")
    for i in range(4):
        j.forward(8)
        j.penup()
        j.forward(29)
        j.pendown()
        j.forward(8)
        j.right(90)
    j.penup()
    #print("rünnak asukoht:", asukoht)


# ründamisaknas kasutatava nupu "Märgista" funktsioon
# märgi tähistus listis 2
def atk_mark():
    global asukoht
    global kaik
    global j

    if not kaik:
        return None

    global lastpress

    if time() - lastpress < 0.05: #0.6
        return None

    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    lastpress = time()

    if mangijap.laud[asukoht[1]][asukoht[0]] == 0:
        #lastpress += 0.1
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

        mangijap.laud[asukoht[1]][asukoht[0]] = 2

    #print("rünnak asukoht:", asukoht)


# ründamisaknas kasutatava nupu "Eemalda märgistus" funktsioon
def atk_unmark():
    global asukoht
    global kaik
    global j

    if not kaik:
        return None

    global lastpress

    ##print(time()-lastpress)

    if time() - lastpress < 0.05: #0.6
        return None

    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])
    lastpress = time()

    if mangijap.laud[asukoht[1]][asukoht[0]] == 2:
        #lastpress += 0.1
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

        mangijap.laud[asukoht[1]][asukoht[0]] = 0

    #print("rünnak asukoht:", asukoht)


# ründamisaknas kasutatava nupu "allahu akbar" funktsioon
def atk_pomm():
    global lastpress
    global asukoht
    global kaik
    global j
    global ajalug
    global kaigunumber
    global mangijatabamus
    global arvutitabamus
    global kogulaevad
    global voit
    global laud

    if not kaik:
        return None

    if time() - lastpress < 0.5: #0.6
        return None
    j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])

    kaigunumber += 1
    lastpress = time()
    # kui on laev
    posx = asukoht[0]
    posy = asukoht[1]
    ajalug.configure(state='normal')
    ajalug.insert(END, str(kaigunumber) + "." + " " * (9 - len(str(kaigunumber))) + numtolet[posx] + " " + str(posy))
    #print(mangijap.laud[posy][posx])
    if mangijap.laud[posy][posx] == 2:
        #print("Mart Helme")
        lastpress -= 0.069
        atk_unmark()

    if arvutil.laud[posy][posx] == 1 and mangijap.laud[posy][posx] == 0:
        j.penup()
        j.goto(125 + 50 * posx, -225 + 50 * posy)
        j.pencolor("#0000FF")
        j.pendown()
        j.dot(23)
        moves = [[0, 1], [1, 0], [-1, 0], [0, -1]]
        for move in moves:
            if posx + move[1] >= 0 and posy + move[0] >= 0 and posx + move[1] <= 9 and posy + move[0] <= 9:
                if mangijap.laud[posy + move[0]][posx + move[1]] == 4:
                    j.pensize(23)
                    j.goto(125 + 50 * (posx + move[1]), -225 + 50 * (posy + move[0]))
                    j.pensize(5)
                    j.pencolor("#FF0000")
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
                    j.goto(125 + 50 * posx, -225 + 50 * posy)
                    j.pencolor("#0000FF")
                    j.pendown()

        j.pencolor("#FF0000")
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
        j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])

        # märgib tabamuse
        mangijap.laud[posy][posx] = 4
        arvutil.laud[posy][posx] = 4
        for laev in arvutil.laevad:
            if [posx, posy] in laev:
                laev.remove([posx, posy])
                if laev:
                    ajalug.insert(END, "  Pihtas")
                else:
                    ajalug.insert(END, "  Pihtas põhjas")
                #print(arvutil.laevad)
                break
        mangijatabamus += 1

    elif mangijap.laud[posy][posx] in [0, 2]:

        # kui ei ole laeva
        j.pencolor("#A9A9A9")
        j.goto(125 + 50 * asukoht[0], -225 + 50 * asukoht[1])
        j.pendown()
        j.dot(15)
        j.penup()
        j.goto(102 + 50 * asukoht[0], -247 + 50 * asukoht[1])

        mangijap.laud[posy][posx] = 3

    elif mangijap.laud[posy][posx] in [3, 4]:
        ajalug.insert(END, "  " + choice(puudalla))

    #print(kogulaevad, "eee")
    ajalug.insert(END, "\n")
    ajalug.yview(END)
    ajalug.configure(state='disabled')

    '''  
    #print("arvutil - arvuti laud arvutile")
    #pp.p#print(arvutil.laud)
    #print("mangijap - arvuti laud mängijale")
    #pp.p#print(mangijap.laud)
    #print("rünnak asukoht:", asukoht)
    '''
    #print(kogulaevad, "eee")
    # kontroll kas mängija on võitnud
    if mangijatabamus == kogulaevad:
        voit = 1
        voiduteade()
        return None
    kaik = False

    #print("Arvuti käik")

    # arvuti mõtleb

    motl = Toplevel(laud)
    motl.title("")
    motl.geometry('200x40')
    motl.protocol("WM_DELETE_WINDOW", noclose)
    motl.resizable(False, False)
    motl1 = Label(motl, text="ARVUTI MÕTLEB")
    motl1.place(x=50, y=10)

    laud.update()
    sleep(0.2 + 5 * random() ** 10)
    motl.destroy()
    ajalug.configure(state='normal')

    # arvuti ründab
    if raskustase == 1:
        atk_veryeasy()
    elif raskustase == 2:
        atk_easy()
    elif raskustase == 3:
        atk_normal()
    elif raskustase == 4:
        atk_hard()
    elif raskustase == 5:
        atk_extreme()
    elif raskustase == 6:
        atk_impossible()

    ajalug.insert(END, "\n")
    ajalug.yview(END)
    ajalug.configure(state='disabled')

    # kontroll kas arvuti on võitnud
    if arvutitabamus == kogulaevad:
        voit = -1
        avalda()
        voiduteade()
    else:
        kaik = True
    #print(mangijatabamus, arvutitabamus, kogulaevad)

def avalda():
    for y in range(10):
        for x in range(10):
            if mangijap.laud[y][x] in [0,2] and arvutil.laud[y][x] == 1:
                mangijap.laud[y][x] = 5
                j.penup()
                j.goto(125 + 50 * x, -225 + 50 * y)
                j.pencolor("#0000FF")
                j.pendown()
                j.dot(23)

                moves = [[0, 1], [1, 0], [-1, 0], [0, -1]]
                for move in moves:
                    if x + move[1] >= 0 and y + move[0] >= 0 and x + move[1] <= 9 and y + move[0] <= 9:
                        if mangijap.laud[y + move[0]][x + move[1]] in [4,5]:
                            j.pendown()
                            j.pensize(23)
                            j.goto(125 + 50 * (x + move[1]), -225 + 50 * (y + move[0]))
                            j.pensize(5)
                            if mangijap.laud[y + move[0]][x + move[1]] == 4:
                                j.pencolor("#FF0000")
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
                            j.goto(125 + 50 * x, -225 + 50 * y)
                            j.pencolor("#0000FF")
                            j.pendown()

def voiduteade():
    global laud
    global hml_save
    global ajalug
    global playerfile

    #print(ajalug)
    if voit == 1:
        mb.showinfo("VÕIT", choice(voidusonumid))
    elif voit == -1:
        mb.showinfo("KAOTUS", choice(kaotussonumid))
    else:
        return None
    teade = Toplevel(laud)
    teade.title("Uuesti?")
    teade.geometry('250x100')
    teade.resizable(False, False)
    teademsg = Label(teade, text="Kas soovid uuesti mängida?")
    teademsg.place(x=50, y=5)
    nupp1 = ttk.Button(teade, text="Jah", command=uusjah)
    nupp1.place(x=90, y=30, width=70)
    nupp2 = ttk.Button(teade, text="Ei", command=uusei)
    nupp2.place(x=90, y=60, width=70)

    # salvesta heatmap?
    open("heatmapl.txt", "w").close()
    #overwrite = open("heatmapl.txt", "w")

    #print("salvestan heatmapi")
    #pp.p#print(hml_save)
    for row in hml_save:
        asi = ""
        for item in row:
            asi += str(item) + " "
        playerfile.write(encode(asi) + "\n")
    #overwrite.close()
    playerfile.close()
    playerfile = open(dir + "/" + kasu + ".txt", "w", encoding="utf-8")
    fail = open("temp.txt","r", encoding="utf-8")
    playerfile.write(fail.read())
    playerfile.close()
    fail.close()

def uusjah():
    global uusmang
    global laud
    global sobib
    uusmang = True
    sobib = True
    laud.destroy()


def uusei():
    global uusmang
    global laud
    uusmang = False
    laud.destroy()


def noclose():
    pass


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
    global ajalug
    global kaigunumber
    global mangijatabamus
    global arvutitabamus
    global kogulaevad
    global voit
    global laud
    global uusmang
    global leitud
    global playerfile

    # sisselogimisaken
    login = Tk()
    login.title("Login")
    login.geometry('300x210')
    login.resizable(False, False)

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

    #playerfile = open(dir + "/" + kasu + ".txt", "r", encoding="utf-8")

    # tervituse aken
    tervitus = Tk()
    tervitus.title("Tere tulemast, " + kasu)
    tervitus.geometry('300x110')
    tervitus.resizable(False, False)
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

    uusmang = True
    while uusmang:
        # valikute tegemise laud ehk
        # mängija laud talle endale kuvatuna
        global valiklaud
        valiklaud = Laud()
        #pp.p#print(valiklaud.laud)

        # kolmas laud (l nagu laev)
        # arvuti laevade informatsiooni
        # ehk arvuti laud "talle kuvatuna"
        global arvutil
        arvutil = Laud()

        # neljas laud (p nagu pomm)
        # arvuti pommitamise informatsiooni (arvuti ründab mängijat)
        global arvutip
        arvutip = Laud()

        # viies laud (p nagu pomm)
        # mängija pommitamise informatsioon ehk
        # arvuti laud mängijale kuvatuna
        global mangijap
        mangijap = Laud()
        # raskustaseme aken
        rask = Tk()
        rask.title("Raskustase")
        rask.geometry('300x230')
        rask.resizable(False, False)
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
        # #print(raskustase)

        # laevavaliku aken
        laevavalik = Tk()
        laevavalik.title("Laevade paigutamine")
        canvas1 = Canvas(master=laevavalik, width=700, height=700)
        canvas1.pack()
        laevavalik.minsize(width=650, height=650)
        laevavalik.maxsize(width=700, height=700)

        canvas = TurtleScreen(canvas1)
        canvas.tracer(0, 0)
        #canvas.tracer(1, 1)

        # rawturtle objekt
        global j
        j = turtle.RawTurtle(canvas)
        j.speed(0)
        j.hideturtle()
        j.pensize(10)
        j.penup()
        for i in range(10):
            j.goto(-225 + 50 * i, -300)
            j.write(numtolet[i], True, "center", ("Arial", 30, "bold"))
        for i in range(11):
            j.goto(-250, -250 + 50 * i)
            j.pendown()
            j.forward(500)
            j.penup()
        j.left(90)
        for i in range(10):
            j.goto(-280, -248 + 50 * i)
            j.write(str(i), True, "left", ("Arial", 30, "bold"))
        for i in range(11):
            j.goto(-250 + 50 * i, -250)
            j.pendown()
            j.forward(500)
            j.penup()
        j.pensize(5)
        j.goto(-248, -247)
        asukoht = [0, 0]
        #canvas.tracer(1, 2)
        j.pencolor("#00FF00")
        j.pendown()
        for i in range(4):
            j.forward(8)
            j.penup()
            j.forward(29)
            j.pendown()
            j.forward(8)
            j.right(90)
        j.penup()

        global control
        control = Toplevel(laevavalik)
        control.title("Paigutaja kontrollimine")
        control.geometry('300x240')
        control.protocol("WM_DELETE_WINDOW", noclose)
        control.resizable(False,False)

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
        #pp.p#print(valiklaud.laud)
        #print()

        for i in mangijal.laud:
            for s in range(10):
                if i[s] == "x":
                    i[s] = 0

        #pp.p#print(mangijal.laud)
        #print()
        #pp.p#print(valiklaud.laud)

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
        #print(valiklaud.laevad)
        valiklaud.laevapikkused = [len(i) for i in valiklaud.laevad]
        #print(valiklaud.laevapikkused)
        kogulaevad = sum(valiklaud.laevapikkused)
        #print(kogulaevad)

        #print("EKRE")

        global hml
        hml = []
        #hmlfile = open("heatmapl.txt", "r").readlines()
        playerfile = open(dir + "/" + kasu + ".txt", "r", encoding="utf-8")
        a = decode(playerfile.readline())
        playerfile.readline()
        #print(a,"oooooo")
        hmlfile = playerfile.readlines()
        playerfile.close()

        playerfile = open("temp.txt", "w", encoding="utf-8")
        #print(encode(a) + "\n")
        playerfile.write(encode(a) + "\n"*2)

        #pp.p#print(hmlfile)
        for i in hmlfile:
            i = decode(i)
            #print(i)
            c = []
            for j in i.strip().split(" "):
                c.append(int(j.strip()))
            hml.append(c)

        global hml_save
        hml_save = deepcopy(hml)
        #print("hml_save")
        #pp.p#print(hml_save)

        global diag
        diag = min(valiklaud.laevapikkused)

        dnl = [
            [[0, 0]],
            [[1, 0], [0, 1]],
            [[2, 0], [1, 1], [0, 2]],
            [[3, 0], [2, 1], [1, 2], [0, 3]],
            [[4, 0], [3, 1], [2, 2], [1, 3], [0, 4]],
            [[5, 0], [4, 1], [3, 2], [2, 3], [1, 4], [0, 5]],
            [[6, 0], [5, 1], [4, 2], [3, 3], [2, 4], [1, 5], [0, 6]],
            [[7, 0], [6, 1], [5, 2], [4, 3], [3, 4], [2, 5], [1, 6], [0, 7]],
            [[8, 0], [7, 1], [6, 2], [5, 3], [4, 4], [3, 5], [2, 6], [1, 7], [0, 8]],
            [[9, 0], [8, 1], [7, 2], [6, 3], [5, 4], [4, 5], [3, 6], [2, 7], [1, 8 ], [0, 9]],
            [[9, 1], [8, 2], [7, 3], [6, 4], [5, 5], [4, 6], [3, 7], [2, 8], [1, 9]],
            [[9, 2], [8, 3], [7, 4], [6, 5], [5, 6], [4, 7], [3, 8], [2, 8]],
            [[9, 3], [8, 4], [7, 5], [6, 6], [5, 7], [4, 8], [3, 9]],
            [[9, 4], [8, 5], [7, 6], [6, 7], [5, 8], [4, 9]],
            [[9, 5], [8, 6], [7, 7], [6, 8], [5, 9]],
            [[9, 6], [8, 7], [7, 8], [6, 9]],
            [[9, 7], [8, 8], [7, 9]],
            [[9, 8], [8, 9]],
            [[9, 9]]
        ]

        global diagonaalid
        diagonaalid = []
        for d in range(0, len(dnl), diag):
            diagonaalid.append(dnl[d])

        leitud = []
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
        laud.title("Laevade ründamine")
        canvas1 = Canvas(master=laud, width=1400, height=700)
        canvas1.pack()
        laud.minsize(width=1350, height=650)
        laud.maxsize(width=1400, height=700)

        canvas = TurtleScreen(canvas1)
        canvas.tracer(0, 0)
        #canvas.tracer(1, 1)

        j = turtle.RawTurtle(canvas)
        j.speed(0)
        j.hideturtle()
        j.pensize(10)
        j.penup()
        for i in range(10):
            j.goto(-575 + 50 * i, -300)
            j.write(numtolet[i], True, "center", ("Arial", 30, "bold"))
        for i in range(11):
            j.goto(-600, -250 + 50 * i)
            j.pendown()
            j.forward(500)
            j.penup()
        j.left(90)
        for i in range(10):
            j.goto(-630, -248 + 50 * i)
            j.write(str(i), True, "left", ("Arial", 30, "bold"))
        for i in range(11):
            j.goto(-600 + 50 * i, -250)
            j.pendown()
            j.forward(500)
            j.penup()
        j.right(90)
        j.goto(-350, 270)
        j.write("SINU LAUD", True, "center", ("Arial", 40, "bold"))
        for i in range(10):
            j.goto(125 + 50 * i, -300)
            j.write(numtolet[i], True, "center", ("Arial", 30, "bold"))
        for i in range(11):
            j.goto(100, -250 + 50 * i)
            j.pendown()
            j.forward(500)
            j.penup()
        j.left(90)
        for i in range(10):
            j.goto(70, -248 + 50 * i)
            j.write(str(i), True, "left", ("Arial", 30, "bold"))
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

        #canvas.tracer(1, 2)
        j.pensize(5)
        j.goto(102, -247)
        asukoht = [0, 0]
        j.pencolor("#00FF00")
        j.pendown()
        for i in range(4):
            j.forward(8)
            j.penup()
            j.forward(29)
            j.pendown()
            j.forward(8)
            j.right(90)
        j.penup()

        # pommitamise kontrollimise aken
        control = Toplevel(laud)
        control.title("Pommitaja kontrollimine")
        control.geometry('300x210')
        control.protocol("WM_DELETE_WINDOW", noclose)
        control.resizable(False,False)
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

        ajal = Toplevel(laud)
        ajal.title("Pommitamisajalugu")
        ajal.protocol("WM_DELETE_WINDOW", noclose)
        ajal.resizable(False, False)
        ajalmsg1 = Label(ajal, text="Sinu käigud")
        ajalmsg1.place(x=89, y=5)
        ajalmsg2 = Label(ajal, text="Arvuti käigud")
        ajalmsg2.place(x=257, y=5)
        ajalug = tkst.ScrolledText(master=ajal, wrap=WORD, width=60, height=11)
        ajalug.pack(padx=10, pady=(25,10), fill=BOTH, expand=True)
        #ajalug.insert(INSERT, " " * 10 + "Sinu käigud" + " " * 10 + "Arvuti käigud" + "\n")
        ajalug.configure(state='disabled')
        kaigunumber = 0
        #print(valiklaud.laevad, arvutil.laevad)
        mangijatabamus = 0
        arvutitabamus = 0
        voit = 0

        sobib = False
        laud.mainloop()

        if not sobib:
            sys.exit()


game_loop()
#print()
#print(encode("Hello World"))
a = base64.b64encode(bytes("Hello World", "utf-8"))
#print(a)
b = base64.b64decode(a)
#print(b)
#print(str(b, "utf-8"))