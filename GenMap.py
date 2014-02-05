from random import randrange
from case import Case
from Modele import *
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
     for y in range(0,self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       self.tab[x,y]= Case(x,y)

    def matriceRandomBasic(self,elt):
     for y in range(0,self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       self.tab[x,y].biome.set(elt,randrange(self.MAXVALUE))

    def matriceRandom0(self,elt): #Bord à 0
     for y in range(0,self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       if x == init or y == 0 or y == self.Y -1 or x == self.X + init -1:
        self.tab[x,y].biome.set(elt,0)
       else: 
        self.tab[x,y].biome.set(elt,randrange(self.MAXVALUE))

    def matriceProgressive(self,elt): #Progressive
     for y in range(0,self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       self.tab[x,y].biome.set(elt,min((self.MAXVALUE * (y))//self.Y, (self.MAXVALUE * (self.Y - (1 + y)))//(self.Y)))

    def cycle(self,duree):
     self.initialise()
     for i in range(0,duree):
      self.Division()
      self.Egalisation()
     self.Finalisation()

    def Division(self,mod = 2):
     aux = {}
     for y in range(0,self.Y):
      init = self.ligne(y)
      offset = 0
      if init * 2 > y:
       offset = 1
      for x in range(init, self.X + init):
       for y2 in range(0,mod):
        init2 =  self.ligne(y2)
        for x2 in range(init2,mod + init2):
         aux[(x)*mod+x2 - offset, y*mod+y2] = Case((x)*mod+x2 -offset,y*mod+y2)
         aux[(x)*mod+x2 - offset, y*mod+y2].biome.copy(self.tab[x,y].biome)
     self.tab = aux
     self.Y *= 2
     self.X *= 2

    def Egalisation(self):
     aux = {}
     for y in range(0,self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       biome = self.Moyenne(x,y)
       aux[x,y] = Case(x,y)
       aux[x,y].biome = biome
     self.tab = aux


    def Moyenne(self,x,y):
     aux = []
     biome = self.tab[x,y].biome
     compteur = 1
     for elt in self.modele.hierarchie:
      biome.set(elt,0)
     for elt in self.tab[x,y].Voisins():
      if elt in self.tab: 
       for elt1 in self.modele.hierarchie:
        biome.add(elt1,self.tab[elt].biome.dict[elt1])
       aux.append(elt)
       compteur = compteur + 1
     x1,y1 =  aux[randrange(compteur - 1)]
     if compteur > 0:
      for elt in biome.dict.keys():
       biome.div(elt,compteur)
       biome.add(elt,self.tab[x1,y1].biome.dict[elt])
       biome.div(elt,2)
     return biome

    def Finalisation(self):
     aux = {}
     self.niveaux = {}
     for i in range(0,self.MAXVALUE):
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

def aff(w,Poney):
 for elt in Poney.tab.values():
  w.draw(elt.sprite())
 w.display()
def cycle(t,l,h): 
 Poney = MapGen(l,h,[])
 Poney.cycle(t)
 i = 0
 return Poney

