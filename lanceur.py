import sfml as sf
from GenMap import *
from hexagone import *
from random import randint,randrange
from os import system
w = sf.RenderTexture(1158,1000)#hexagone.l * X + hexagone.l * 0.5 / (hexagone.L * 1.5) *( Y / 2)
w.clear()
def boucle(t,d):
 w = sf.RenderWindow(sf.VideoMode(1,1),"LOLWUT")
 w.clear()
 while 1>0:
  a = cycle(t,d)
  aff(w,a)
  print(a.X)
  print(a.Y)

def GenerateI(nb,minX,minY,maxX,maxY,it = 2):
 for i in range(nb):
  system("clear")
  print("[>] Work on {0}".format(i))
  print("    Generation")
  map = GenerateMap(it,randint(minX,maxX),randint(minY,maxY))
  print("    Texture")
  w = map.getTexture()
  print("    Save")
  map.save("map{0}.png".format(i))
