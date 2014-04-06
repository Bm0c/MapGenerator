from random import randrange,randint
from case import Case
from Modele import *
from hexagone import *
from tableau import Tableau
from genRegion import GenRegionVoronoi

class Seed:

    def __init__(self,largeur,hauteur,noeud = {"type" : "plaque"},minValue = 0,maxValue = 255, value = 0):
     self.function = {"rand" : self.rand, "degrade" : self.degrade, "islande" : self.islande ,"plaque" : self.plaque}
     self.maxValue = maxValue
     self.minValue = minValue
     self.X = largeur
     self.Y = hauteur
     self.tab = Tableau(self.X,self.Y)
     if "args" in noeud:
      self.function[noeud["type"]](noeud["args"])
     else :
      self.function[noeud["type"]]()

    def degrade(self,args = {"direction":"Y","evolution":"increase"}):
     if args["direction"] == "Y":
      c = self.Y
      current = lambda x,y : y
     else:
      c =  self.X 
      current = lambda x,y : x - self.ligne(y) 
     if args["evolution"] == "increase":
      fun = lambda x,y : self.maxValue * current(x,y) // c
     elif args["evolution"] == "decrease":
      fun = lambda x,y : self.maxValue * (c - (1 + current(x,y))) // c
     elif args["evolution"] == "center":
      fun = lambda x,y : min(self.maxValue * current(x,y) // c,self.maxValue * (c - (1 + current(x,y))) //c) * 2
     elif args["evolution"] == "border":
      fun = lambda x,y : max(self.maxValue * current(x,y) // c,self.maxValue * (c - (1 + current(x,y))) //c) - ( self.maxValue // 2) * 2
     for(x,y) in self.tab.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = fun(x,y) 

    def rand(self,args = {}):
     for(x,y) in self.tab.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = randint(self.minValue,self.maxValue) 

    def islande(self,args = (2,[100,95,80,60,0])):
     for x,y in self.tab.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = self.minValue 
     liste = [ elt for elt in self.tab.iterB() ]
     le = len(liste)
     nb , li = args
     sup = li[0] 
     inf = li[1]
     aux = []
     for i in range(nb):
      l = [ elt for elt in self.tab.iterB(1) ]
      elt = l[randrange(len(l))]
      self.tab[elt].value = randint(inf  * self.maxValue  // 100, sup * self.maxValue // 100)
      aux = aux + [ v for v in self.tab[elt].Voisins() if v in liste  ]
      if elt in liste:
       liste.remove(elt)
      l.remove(elt)
     current = nb
     for inf_ in li[2:]:
      sup = inf
      inf = inf_ 
      for i in range((sup - inf)  * le // 100) :
       for y in range(10):
        current = aux[randrange(len(aux))]
        aux.remove(current)
        if current in liste:
         liste.remove(current)
         self.tab[current].value = randint(inf *  self.maxValue //100,sup * self.maxValue // 100) 
         aux = aux + [ elt for elt in self.tab[current].Voisins() if elt in liste  ]
         break

    def plaque(self,args = {"nombre" : 5, "plaques" : 8}):
     for x,y in self.tab.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = 0 #randrange(self.minValue , (self.minValue + self.maxValue // 2) )
     liste = [ elt for elt in self.tab.iterB(2) ]
     nombre = int(args["nombre"])
     plaque = int(args["plaques"])
     plaques = GenRegionVoronoi(self.tab.X,self.tab.Y,nb = plaque)
     liste_plaque = [ (elt.interieur,elt.frontiere) for elt in plaques.regions]
     for i in range(nombre):
      li,lf = liste_plaque[randrange(len(liste_plaque))]
      liste_plaque.remove((li,lf))
      l = [ (elt.u,elt.v)  for elt in li if (elt.u,elt.v) in liste]
      for elt in l:
       self.tab[elt].value = randint((self.minValue + self.maxValue)  * 3 // 4 , self.maxValue )
