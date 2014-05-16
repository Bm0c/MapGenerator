from random import randint
from monde import Monde
from hexagone import hexagone

def GenerateI(nb,minX,minY,maxX,maxY,it = 2,size = 16):
    hexagone.setl(size)
    for i in range(nb):
        print("[>] Work on {0}".format(i))
        map = Monde(randint(minX,maxX),randint(minY,maxY),"patron.xml",it)
        print("Save")
        map.save("map{0}.png".format(i))

def fun():
    GenerateI(10,10,10,11,11)
