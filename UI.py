from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter.scrolledtext as tkst
import turtle
import base64
import os
from time import time


dir = "./playerdata"
try:
    os.listdir(dir)
except:
    os.mkdir(dir)


vot = "Laseme kõik laevad õhku"

def encode(string):
    return str(base64.b64encode(bytes(string, "utf-8")), "utf-8")
def decode(string):
    return str(base64.b64decode(bytes(string, "utf-8")), "utf-8")


def logi():
    global playerdata
    global kasu
    global sobib
    kasu = str(kasutaja.get())
    paro = str(parool.get())
    #print(kasu,paro)
    if "" in [kasu,paro]:
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

def lokas():
    kasu = str(kasutaja1.get())
    paro = str(parool1.get())
    #print(kasu, paro)
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

def reeg():
    r = Toplevel(tervitus)
    r.title("Reeglid")
    reeglid = tkst.ScrolledText(master=r, wrap=WORD, width=50, height=10)
    reeglid.pack(padx=10, pady=10, fill=BOTH, expand=True)
    # Adding some text, to see if scroll is working as we expect it
    sis = open("Reeglid.txt","r")
    reeglid.insert(INSERT, sis.read())
    sis.close()

def mang():
    global sobib
    sobib = True
    tervitus.destroy()

def rt(n):
    global sobib
    global raskustase
    sobib = True
    raskustase = n
    rask.destroy()

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
print(raskustase)


def ules():
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    #print(asukoht)
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


def alla():
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    #print(asukoht)
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

def vasakule():
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    #print(asukoht)
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

def paremale():
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    #print(asukoht)
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

def paiguta():
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time() + 0.3
    x = asukoht[0]
    y = asukoht[1]
    if valiklaud[y][x] == 0:
        valiklaud[y][x] = 1
        j.goto(-225 + 50 * x, -225 + 50 * y)
        j.pencolor("#0000FF")
        j.pendown()
        j.dot(23)
        j.penup()
        for i in [[x+1,y+1],[x+1,y-1],[x-1,y+1],[x-1,y-1]]:
            if not (i[0] < 0 or i[1] < 0 or i[0] > 9 or i[1] > 9):
                if valiklaud[i[1]][i[0]] == 0:
                    rist([i[0],i[1]])
                    valiklaud[i[1]][i[0]] = "x"
        suund = 0
        if (x > 0 and valiklaud[y][x-1] == 1) or (x < 9 and valiklaud[y][x+1] == 1):
            suund = "h"
        elif (x == 0 and valiklaud[y][x+1] == 1) or (x == 9 and valiklaud[y][x-1] == 1):
            suund = "h"
        elif (y > 0 and valiklaud[y-1][x] == 1) or (y < 9 and valiklaud[y+1][x] == 1):
            suund = "v"
        elif (y == 0 and valiklaud[y+1][x] == 1) or (y == 9 and valiklaud[y-1][x] == 1):
            suund = "v"
        print(suund)
        if suund == "h":
            ots1 = x
            ots2 = x
            while ots1 > 0 and valiklaud[y][ots1 - 1] == 1:
                ots1 -= 1
            while ots2 < 9 and valiklaud[y][ots2 + 1] == 1:
                ots2 += 1
            print(ots1,ots2)
            a = 2
            juures1 = 0
            juures2 = 0
            while ots1 - a >= 0:
                try:
                    if valiklaud[y][ots1 - a] == 1:
                        a += 1
                        juures1 += 1
                    else:
                        break
                except IndexError:
                    break
            a = 2
            while ots2 + a <= 9:
                try:
                    if valiklaud[y][ots2 + a] == 1:
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
                    if valiklaud[y][ots1 - 1] == 0:
                        rist([ots1 - 1, y])
                        valiklaud[y][ots1 - 1] = "x"
            if l + juures2 >= 5:
                if ots2 < 9:
                    if valiklaud[y][ots2 + 1] == 0:
                        rist([ots2 + 1, y])
                        valiklaud[y][ots2 + 1] = "x"
        elif suund == "v":
            ots1 = y
            ots2 = y
            while ots1 > 0 and valiklaud[ots1 - 1][x] == 1:
                ots1 -= 1
            while ots2 < 9 and valiklaud[ots2 + 1][x] == 1:
                ots2 += 1
            print(ots1, ots2)
            a = 2
            juures1 = 0
            juures2 = 0
            while ots1 - a >= 0:
                try:
                    if valiklaud[ots1 - a][x] == 1:
                        a += 1
                        juures1 += 1
                    else:
                        break
                except IndexError:
                    break
            a = 2
            while ots2 + a <= 9:
                try:
                    if valiklaud[ots2 + a][x] == 1:
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
                    if valiklaud[ots1 - 1][x] == 0:
                        rist([x, ots1 - 1])
                        valiklaud[ots1 - 1][x] = "x"
            if l + juures2 >= 5:
                if ots2 < 9:
                    if valiklaud[ots2 + 1][x] == 0:
                        rist([x, ots2 + 1])
                        valiklaud[ots2 + 1][x] = "x"
        else:
            a = 2
            juures1 = 0
            juures2 = 0
            while x - a >= 0:
                try:
                    if valiklaud[y][x - a] == 1:
                        a += 1
                        juures1 += 1
                    else:
                        break
                except IndexError:
                    break
            a = 2
            while x + a <= 9:
                try:
                    if valiklaud[y][x + a] == 1:
                        a += 1
                        juures2 += 1
                    else:
                        break
                except IndexError:
                    break

            print(juures1, juures2)
            if juures1 >= 4:
                if x > 0:
                    if valiklaud[y][x - 1] == 0:
                        rist([x - 1, y])
                        valiklaud[y][x - 1] = "x"
            if juures2 >= 4:
                if x < 9:
                    if valiklaud[y][x + 1] == 0:
                        rist([x + 1, y])
                        valiklaud[y][x + 1] = "x"

            a = 2
            juures1 = 0
            juures2 = 0
            while y - a >= 0:
                try:
                    if valiklaud[y - a][x] == 1:
                        a += 1
                        juures1 += 1
                    else:
                        break
                except IndexError:
                    break
            a = 2
            while y + a <= 9:
                try:
                    if valiklaud[y + a][x] == 1:
                        a += 1
                        juures2 += 1
                    else:
                        break
                except IndexError:
                    break

            print(juures1, juures2)
            if juures1 >= 4:
                if y > 0:
                    if valiklaud[y - 1][x] == 0:
                        rist([x, y - 1])
                        valiklaud[y - 1][x] = "x"
            if juures2 >= 4:
                if y < 9:
                    if valiklaud[y + 1][x] == 0:
                        rist([x, y + 1])
                        valiklaud[y + 1][x] = "x"

        j.goto(-248 + 50 * x, -247 + 50 * y)

def eemalda():
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time() + 0.3
    x = asukoht[0]
    y = asukoht[1]
    if valiklaud[y][x] == 1:
        valiklaud[y][x] = 0
        j.goto(-225 + 50 * x, -225 + 50 * y)
        j.pencolor("#FFFFFF")
        j.pendown()
        j.dot(23)
        j.penup()
        for i in [[x+1,y+1],[x+1,y-1],[x-1,y+1],[x-1,y-1]]:
            if not (i[0] < 0 or i[1] < 0 or i[0] > 9 or i[1] > 9):
                if valiklaud[i[1]][i[0]] == "x":
                    lsd = []
                    if i[1] < 9:
                        if i[0] < 9:
                            lsd.append(valiklaud[i[1]+1][i[0]+1])
                        if i[0] > 0:
                            lsd.append(valiklaud[i[1]+1][i[0]-1])
                    if i[1] > 0:
                        if i[0] < 9:
                            lsd.append(valiklaud[i[1]-1][i[0]+1])
                        if i[0] > 0:
                            lsd.append(valiklaud[i[1]-1][i[0]-1])
                    if 1 not in lsd:
                        unrist([i[0],i[1]])
                        valiklaud[i[1]][i[0]] = 0
                    del lsd

        ots1 = x
        while ots1 > 0 and valiklaud[y][ots1 - 1] == 1:
            ots1 -= 1
        ots2 = y
        while ots2 > 0 and valiklaud[ots2 - 1][x] == 1:
            ots2 -= 1
        ots3 = x
        while ots3 < 9 and valiklaud[y][ots3 + 1] == 1:
            ots3 += 1
        ots4 = y
        while ots4 < 9 and valiklaud[ots4 + 1][x] == 1:
            ots4 += 1
        print(ots1,ots2,ots3,ots4)

        if x - ots1 <= 4 and ots1 > 0:
            if valiklaud[y][ots1-1] == "x":
                lsd = []
                if y < 9:
                    if ots1-1 < 9:
                        lsd.append(valiklaud[y + 1][ots1])
                    if ots1-1 > 0:
                        lsd.append(valiklaud[y + 1][ots1-2])
                if y > 0:
                    if ots1-1 < 9:
                        lsd.append(valiklaud[y - 1][ots1])
                    if ots1-1 > 0:
                        lsd.append(valiklaud[y - 1][ots1-2])
                if 1 not in lsd:
                    unrist([ots1-1, y])
                    valiklaud[y][ots1-1] = 0
                del lsd
        if ots3 - x <= 4 and ots3 < 9:
            if valiklaud[y][ots3+1] == "x":
                lsd = []
                if y < 9:
                    if ots3+1 < 9:
                        lsd.append(valiklaud[y + 1][ots3+2])
                    if ots3+1 > 0:
                        lsd.append(valiklaud[y + 1][ots3])
                if y > 0:
                    if ots3+1 < 9:
                        lsd.append(valiklaud[y - 1][ots3+2])
                    if ots3+1 > 0:
                        lsd.append(valiklaud[y - 1][ots3])
                if 1 not in lsd:
                    unrist([ots3+1, y])
                    valiklaud[y][ots3+1] = 0
                del lsd
        if y - ots2 <= 4 and ots2 > 0:
            if valiklaud[ots2-1][x] == "x":
                lsd = []
                if ots2-1 < 9:
                    if x < 9:
                        lsd.append(valiklaud[ots2][x+1])
                    if x > 0:
                        lsd.append(valiklaud[ots2][x-1])
                if ots2-1 > 0:
                    if x < 9:
                        lsd.append(valiklaud[ots2-2][x+1])
                    if x > 0:
                        lsd.append(valiklaud[ots2-2][x-1])
                if 1 not in lsd:
                    unrist([x, ots2-1])
                    valiklaud[ots2-1][x] = 0
                del lsd
        if ots4 - y <= 4 and ots4 < 9:
            if valiklaud[ots4+1][x] == "x":
                lsd = []
                if ots4+1 < 9:
                    if x < 9:
                        lsd.append(valiklaud[ots4+2][x+1])
                    if x > 0:
                        lsd.append(valiklaud[ots4+2][x-1])
                if ots4+1 > 0:
                    if x < 9:
                        lsd.append(valiklaud[ots4][x+1])
                    if x > 0:
                        lsd.append(valiklaud[ots4][x-1])
                if 1 not in lsd:
                    unrist([x, ots4+1])
                    valiklaud[ots4+1][x] = 0
                del lsd


        j.goto(-248 + 50 * x, -247 + 50 * y)

def rist(asuk):
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

def unrist(asuk):
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

def valm1():
    if 1 in [i for e in valiklaud for i in e]:
        global valm
        valm = Toplevel(control)
        valm.title("Oled sa kindel?")
        valm.geometry('300x80')

        msg = Label(valm, text="Oled sa kindel?")
        msg.place(x=100, y=5)
        nupp2 = ttk.Button(valm, text="JAH", command=valm2)
        nupp2.place(x=75, y=40, width=75)
        nupp3 = ttk.Button(valm, text="EI", command=lambda: valm.destroy())
        nupp3.place(x=150, y=40, width=75)
    else:
        mb.showerror("ERROR","Laual ei ole ühtegi laeva.")

def valm2():
    global sobib
    global valm
    sobib = True
    valm.destroy()
    control.destroy()
    laevavalik.destroy()




laevavalik = Tk()
laevavalik.title("Laevade paigutamine")
canvas = Canvas(master = laevavalik, width = 700, height = 700)
canvas.pack()

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
    j.goto(-250+50*i,-250)
    j.pendown()
    j.forward(500)
    j.penup()
j.pensize(5)
j.goto(-248,-247)
asukoht = [0,0]
j.pencolor("#00FF00")
j.pendown()
for i in range(4):
    j.forward(45)
    j.right(90)
j.penup()

control = Toplevel(laevavalik)
control.title("Paigutaja kontrollimine")
control.geometry('300x240')

lastpress = 0
nupp1 = ttk.Button(control, text="N", command=ules)
nupp1.place(x=75, y=20, width=150)
nupp2 = ttk.Button(control, text="W", command=vasakule)
nupp2.place(x=75, y=45, width=75)
nupp3 = ttk.Button(control, text="E", command=paremale)
nupp3.place(x=150, y=45, width=75)
nupp4 = ttk.Button(control, text="S", command=alla)
nupp4.place(x=75, y=70, width=150)
nupp5 = ttk.Button(control, text="Paiguta", command=paiguta)
nupp5.place(x=75, y=120, width=150)
nupp6 = ttk.Button(control, text="Eemalda", command=eemalda)
nupp6.place(x=75, y=145, width=150)
nupp7 = ttk.Button(control, text="Valmis", command=valm1)
nupp7.place(x=75, y=200, width=150)
valiklaud = [[0 for i in range(10)] for j in range(10)]
print(valiklaud)

sobib = False
laevavalik.mainloop()
if not sobib:
    sys.exit()
print(valiklaud)

kaidud = []
laevad = []
for y in range(10):
    for x in range(10):
        if valiklaud[y][x] == 1 and [x,y] not in kaidud:
            laev = [[x,y]]
            kaidud.append([x,y])
            a = 1
            while x + a <= 9:
                if valiklaud[y][x+a] == 1:
                    laev.append([x+a, y])
                    kaidud.append([x+a, y])
                    a += 1
                else:
                    break
            a = 1
            while y + a <= 9:
                if valiklaud[y+a][x] == 1:
                    laev.append([x, y+a])
                    kaidud.append([x, y+a])
                    a += 1
                else:
                    break
            laevad.append(laev)
print(laevad)
laevapikkused = [len(i) for i in laevad]
print(laevapikkused)


def ules():
    if not kaik:
        return None
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    #print(asukoht)
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


def alla():
    if not kaik:
        return None
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    #print(asukoht)
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

def vasakule():
    if not kaik:
        return None
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    #print(asukoht)
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

def paremale():
    if not kaik:
        return None
    global lastpress
    if time() - lastpress < 0.6:
        return None
    lastpress = time()
    j.pendown()
    #print(asukoht)
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

def mark():
    if not kaik:
        return None
    global lastpress
    lastpress += 0.1
    j.pencolor("#FF0000")
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

def unmark():
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

def pomm():
    if not kaik:
        return None
    pass


laud = Tk()
laud.title("Laevade paigutamine")
canvas = Canvas(master = laud, width = 1400, height = 700)
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
    j.goto(-600 + 50 * i,-250)
    j.pendown()
    j.forward(500)
    j.penup()
j.right(90)
j.goto(-350,270)
j.write("SINU LAUD",True,"center",("Arial",40,"bold"))
for i in range(11):
    j.goto(100, -250 + 50 * i)
    j.pendown()
    j.forward(500)
    j.penup()
j.left(90)
for i in range(11):
    j.goto(100 + 50 * i,-250)
    j.pendown()
    j.forward(500)
    j.penup()
j.goto(350,270)
j.write("ARVUTI LAUD",False,"center",("Arial",40,"bold"))

j.pencolor("#0000FF")
j.pensize(23)
for i in laevad:
    j.goto(-575 + 50 * i[0][0], -225 + 50 * i[0][1])
    j.pendown()
    for e in range(len(i)):
        j.goto(-575 + 50 * i[e][0], -225 + 50 * i[e][1])
    j.penup()

j.pensize(5)
j.goto(102,-247)
asukoht = [0,0]
j.pencolor("#00FF00")
j.pendown()
for i in range(4):
    j.forward(45)
    j.right(90)
j.penup()

control = Toplevel(laud)
control.title("Pommitaja kontrollimine")
control.geometry('300x210')
nupp1 = ttk.Button(control, text="N", command=ules)
nupp1.place(x=75, y=20, width=150)
nupp2 = ttk.Button(control, text="W", command=vasakule)
nupp2.place(x=75, y=45, width=75)
nupp3 = ttk.Button(control, text="E", command=paremale)
nupp3.place(x=150, y=45, width=75)
nupp4 = ttk.Button(control, text="S", command=alla)
nupp4.place(x=75, y=70, width=150)
nupp5 = ttk.Button(control, text="Märgista", command=mark)
nupp5.place(x=75, y=120, width=150)
nupp6 = ttk.Button(control, text="Eemalda märgistus", command=unmark)
nupp6.place(x=75, y=145, width=150)
nupp7 = ttk.Button(control, text="Allahu akbar!", command=pomm)
nupp7.place(x=75, y=170, width=150)

kaik = True
laud.mainloop()

print()
print(encode("Hello World"))
a = base64.b64encode(bytes("Hello World", "utf-8"))
print(a)
b = base64.b64decode(a)
print(b)
print(str(b,"utf-8"))
