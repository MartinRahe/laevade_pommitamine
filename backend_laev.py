import pprint
from random import randint

# global muutujad
difficulty = 'normal' #Default difficulty

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
mangijah.print_laud()

# teine laud (l nagu laev)
mangijal = Laud(10,10) #Siin hoitakse mängija laevade informatsiooni
mangijal.print_laud()

# kolmas laud (l nagu laev)
arvutil = Laud(10,10) #Siin hoitakse arvuti laevade informatsiooni
arvutil.print_laud()

# neljas laud (p nagu pomm)
arvutip = Laud(10,10) #Siin hoitakse arvuti pommitamise informatsiooni
arvutip.print_laud()

# viies laud (p nagu pomm)
mangijap = Laud(10,10) #Siin hoitakse mängija pommitamise informatsiooni
mangijap.print_laud()
#------------------------------

#Easy: KKK teeb ää
def easyak47(): #Lihtsa raskustaseme arvuti tulistamiskäik
  x = randint(0,mangijal.pikkus) 
  y = randint(0,mangijal.laius)
  while arvutip[y][x] == 'O' or arvutip[y][x] == 'x': 
    x = randint(0,9)
    y = randint(0,9)
  if mangijal[y][x] == '@':
    arvutip[y][x] = 'x'
  else:
    arvutip[y][x] = 'O'
  
#Normal:

#Hard:

#Extreme:

#Impossible: KKK teeb ää
if difficulty == 'impossible':
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
      arvutip.laud[koord[0][0]][koord[0][1]] = 'x'
      koord.pop(0)