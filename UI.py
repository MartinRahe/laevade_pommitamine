from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter.scrolledtext as tkst
import turtle
import base64
import os


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
    r = Tk()
    r.title("Reeglid")
    reeglid = tkst.ScrolledText(master=r, wrap=WORD, width=50, height=10)
    reeglid.pack(padx=10, pady=10, fill=BOTH, expand=True)
    # Adding some text, to see if scroll is working as we expect it
    reeglid.insert(INSERT,
"""1. Mängitakse 10x10 ruudustikul, käigud toimuvad ruutude sees.
2. Mängu alguses peab mängija lauale paigutama oma laevad. Laevu peab olema vähemalt üks ja laeva maksimaalne pikkus on 5 ruutu.
3. Ükski kaks laeva ei tohi omada ühist ruutu, serva ega tippu.
4. Kui mängija on oma laevad paigutanud, paigutab arvuti oma lauale samasugused laevad.
5. Mängija ja arvuti ei näe üksteise laevu.
6. Pommitamine käib kordamööda, alustab mängija.
7. Iga käigu järel saavad nii mängija kui arvuti selle kohta tagasisidet.
8. Võidab see, kes hävitab enne kõik vastase laevad."""
                    )

def mang():
    tervitus.destroy()

def rt(n):
    print(n)

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
if sobib:
    pass
else:
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
tervitus.mainloop()

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
rask.mainloop()

print(encode("Hello World"))
a = base64.b64encode(bytes("Hello World", "utf-8"))
print(a)
b = base64.b64decode(a)
print(b)
print(str(b,"utf-8"))
