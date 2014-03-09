import random
from random import randrange
from case import Case
from Modele import *
from hexagone import *

class MapGen:
    

    def __init__(self,largeur,hauteur,modele): #X,Y,Liste_Coeff
     self.X = largeur
     self.Y = hauteur
     self.MAXVALUE = 256
     self.tab = {}
     a = Make("patron")
     a.make()
     self.modele = a.modele
     self.makeMatrice()
     self.initialise()

    def initialise(self):
     types = {}
     types[""] = self.matriceRandomBasic
     types["bords"] = self.matriceRandom0
     types["lignes"] = self.matriceProgressive
     for elt in self.modele.hierarchie:
      types[self.modele.type[elt]](elt)
      
    def ligne (self,y): 
     return (y+1)//2
    
    def makeMatrice(self):
     for y in range(self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       self.tab[x,y]= Case(x,y)
       for elt in self.modele.hierarchie:
        self.tab[x,y].biome.set(elt,0)

    def matriceRandomBasic(self,elt):
     for y in range(self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       self.tab[x,y].biome.set(elt,randrange(self.MAXVALUE))

    def matriceRandom0(self,elt): #Bord à 0
     for y in range(self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       if x == init or y == 0 or y == self.Y -1 or x == self.X + init -1:
        self.tab[x,y].biome.set(elt,0)
       else: 
        if randrange(2) == 1:
         self.tab[x,y].biome.set(elt,randrange(self.MAXVALUE - 1))
        else:
         self.tab[x,y].biome.set(elt,0)

    def matriceProgressive(self,elt): #Progressive
     for y in range(self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       self.tab[x,y].biome.set(elt,min((self.MAXVALUE * (y))//self.Y, (self.MAXVALUE * (self.Y - (1 + y)))//(self.Y)))

    def cycle(self,duree):
     for i in range(duree):
      self.Division()
      self.Egalisation()
     self.Finalisation()

    def Division(self,mod = 2):
     aux = {}
     for y in range(self.Y):
      init = self.ligne(y)
      offset = 0
      if init * 2 > y:
       offset = 1
      for x in range(init, self.X + init):
       for y2 in range(mod):
        init2 =  self.ligne(y2)
        for x2 in range(init2,mod + init2):
         aux[(x)*mod+x2 - offset, y*mod+y2] = Case((x)*mod+x2 -offset,y*mod+y2)
         aux[(x)*mod+x2 - offset, y*mod+y2].biome.copy(self.tab[x,y].biome)
     self.tab = aux
     self.Y *= 2
     self.X *= 2

    def Egalisation(self):
     aux = {}
     for y in range(self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       biome = self.Moyenne(x,y)
       aux[x,y] = Case(x,y)
       aux[x,y].biome = biome
     self.tab = aux


    def Moyenne(self,x,y):
     aux = []
     biome = Biome()
     compteur = 0
     for elt in self.modele.hierarchie:
      biome.set(elt,0)
     for elt in self.tab[x,y].Voisins():
      if elt in self.tab: 
       for elt1 in self.modele.hierarchie:
        biome.add(elt1,self.tab[elt].biome.dict[elt1])
       aux.append(elt)
       compteur = compteur + 1
     x1,y1 =  aux[randrange(compteur)]
     if compteur > 0:
      for elt in biome.dict.keys():
       biome.div(elt,compteur)
       biome.add(elt,self.tab[x1,y1].biome.dict[elt])
       biome.div(elt,2)
     return biome

    def Finalisation(self):
     aux = {}
     self.niveaux = {}
     for i in range(self.MAXVALUE):
      for elt in self.modele.hierarchie:
       aux[elt,i] = 0
     for case in self.tab.values():
      for elt in self.modele.hierarchie:
       aux[elt,case.biome.dict[elt]] += 1
     for elt in self.modele.hierarchie:
      self.niveaux[elt] = []
      i = 0
      buffer_ = 1
      for valeur in self.modele.pourcents[elt]:
       valeur = float(valeur)
       while(i < self.MAXVALUE and buffer_*100/(self.X*self.Y) <= valeur):
        buffer_ += aux[elt,i]
        i+=1
       self.niveaux[elt].append(i)
     for case in self.tab.values():
      for elt in self.modele.hierarchie:
       i = 0
       while i < len(self.niveaux[elt]) and case.biome.dict[elt] > self.niveaux[elt][i]:
        i += 1
       case.biome.dict[elt] = i
      self.modele.determine(case.biome)

    def getTexture(self):
     w = sf.RenderTexture(hexagone.l * self.X + hexagone.l // 2,(hexagone.L * 1.5) * (self.Y // 2 + 1))
     w.clear()
     for elt in self.tab.values():
      w.draw(elt.sprite())
     w.display()
     return w
    
    def save(self,name):
     w = self.getTexture()
     image =  w.texture.to_image()
     image.to_file(name)
    
    def addMap(self,map,i,j):
     i = i + self.ligne(j)
     for x,y in map.tab.keys():
      self.tab[i + x ,y+j].biome.addBiome(map.tab[x,y].biome)

    def moyMap(self,map,i,j):
     i = i + self.ligne(j)
     for x,y in map.tab.keys():
      self.tab[i + x ,y+j].biome.moyBiome(map.tab[x,y].biome)

def GenerateMap(n,x,y,nb):
 map = MapGen(x,y,42)
 for i in range(nb):
  aux = MapGen(x//3,y//3,24)
  map.addMap(aux,random.randrange(x-x//3),random.randrange(y-y//3))
 map.cycle(n)
 return map

def aff(w,Poney):
 for elt in Poney.tab.values():
  w.draw(elt.sprite())
 w.display()

def cycle(t,l,h): 
 Poney = MapGen(l,h,[])
 Poney.cycle(t)
 return Poney
