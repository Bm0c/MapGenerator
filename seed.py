from random import randrange,randint
from case import Case
from Modele import *
from hexagone import *
from tableau import Tableau
from genRegion import GenRegionVoronoi,GenRegionPasse

class Seed:

    def __init__(self,largeur,hauteur,noeud = {"type" : "plaque"},minValue = 0,maxValue = 255, value = 0):
        self.function = {"rand" : self.rand, "degrade" : self.degrade, "plaque" : self.plaque}
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

    def plaque(self,args = {"nombre" : 5, "plaques" : 8}):
        for x,y in self.tab.iterC():
            self.tab[x,y] = Case(x,y)
            self.tab[x,y].value = 0
        liste = [ elt for elt in self.tab.iterB(1) ]
        nombre = args["nombre"]
        plaque = args["plaques"]
        plaques = GenRegionPasse(self.tab,None,plaque,5)
        plaques.finalisation()
        liste_plaque = [ (elt.interieur,elt.frontiere) for elt in plaques.regions]
        for i in range(nombre):
            li,lf = liste_plaque[randrange(len(liste_plaque))]
            liste_plaque.remove((li,lf))
            for elt in [ (elt.u,elt.v)  for elt in li if (elt.u,elt.v) in liste]:
                #self.tab[elt].value = randint((self.minValue + self.maxValue)  * 3 // 4 , self.maxValue )
                self.tab[elt].value = int(((plaques.iteration - self.tab[elt].nb + 1) / plaques.iteration)* self.maxValue)
