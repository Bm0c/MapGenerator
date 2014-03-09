import random
import sfml as sf
from GenMap import *
from hexagone import *
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

def Generate(t,l,h,n):
 for i in range(n):
  print("Working on {0}...".format(i))
  a = cycle(t,l,h)
  a.save("map{0}.png".format(i))

def GenerateI(nb,minX,minY,maxX,maxY):
 for i in range(nb):
  print(" -> Work on {0}".format(i))
  map = GenerateMap(3,random.randint(minX,maxX),random.randint(minY,maxY),random.randint(2,6))
  map.save("map{0}.png".format(i))
