import pprint
from random import randint
from math import floor

# global muutujad
difficulty = 'normal' #Default difficulty
heatmapl = [] #Mängija laevade heatmap
heatmapt = [] #Mängija tulistamise heatmap
tulnim = [] #Nimekiri kohtadest, mida tulistada

class Laud:

  def __init__(self, pikkus, laius):
    self.pikkus = pikkus
    self.laius = laius
    self.laud = [[0 for i in range(self.pikkus)] for j in range(self.laius)] #<3<3 tundus nagu parem variant

# 0,0 0,1 0,2 ...
# 1,0 1,1 1,2 ...
# ...
  def print_laud(self):
    pp  = pprint.PrettyPrinter(indent=4)
    pp.pprint(self.laud)
    print()

#------------------------------
# esimene laud (h nagu heatmap)
mangijah = Laud(10, 10) #Siin hoitakse mängija heatmapi
#mangijah.print_laud()

# teine laud (l nagu laev)
mangijal = Laud(10,10) #Siin hoitakse mängija laevade informatsiooni
#mangijal.print_laud()

# kolmas laud (l nagu laev)
arvutil = Laud(10,10) #Siin hoitakse arvuti laevade informatsiooni
#arvutil.print_laud()

# neljas laud (p nagu pomm)
arvutip = Laud(10,10) #Siin hoitakse arvuti pommitamise informatsiooni
#arvutip.print_laud()

# viies laud (p nagu pomm)
mangijap = Laud(10,10) #Siin hoitakse mängija pommitamise informatsiooni
#mangijap.print_laud()
#------------------------------

heatmapl = Laud(10, 10)
heatmapt = Laud(10, 10)

heatmapl.laud[8][4] = 1

def hardal():
    global tulnim
    hml = [] #koopia heatmapist, mida võib editida
    for i in range(10):
        hml += heatmapl.laud[i]
    print(hml)
    for i in range(len(hml)):
        z = hml.index(max(hml))
        tulnim.append([floor(z/10), z%10, heatmapl.laud[floor(z/10)][(z)%10]])
        hml[z] = -420
    tulnim = sorted(tulnim, key=lambda tul: tul[2], reverse = True)
    print(tulnim)
    print(hml)
    if mangijal.laud[tulnim[0][0]][tulnim[0][1]] == 1:
        arvutip.laud[tulnim[0][0]][tulnim[0][1]] = 'x'
    else:
        arvutip.laud[tulnim[0][0]][tulnim[0][1]] = 'O'
    '''if tulnim = []:
        for i in range(len(hml)):
            hml.index(max(hml))'''
hardal()
arvutip.print_laud()
