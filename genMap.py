from random import randrange,randint
from case import Case
from Modele import *
from hexagone import *
from tableau import Tableau
from seed import Seed

class MapGen():

    def __init__(self,largeur,hauteur,modele): #X,Y,Liste_Coeff
     self.X = largeur
     self.Y = hauteur
     self.MAXVALUE = 256
     self.tab = Tableau(self.X,self.Y)
     self.modele = Modele("patron.xml")
     self.seed = [ (key, Seed(self.X,self.Y,elt["seed"])) for key,elt in self.modele.racine["couche"].items() ]
     for x,y in self.tab.iterC():
      self.tab[x,y] = Case(x,y)
      for key,s in self.seed:
       self.tab[x,y].biome.set(key,s.tab[x,y].value)

    def cycle(self,duree):
     for i in range(duree):
      print("Iter " + str(i))
      print("Division")
      self.Division()
      print("Egalisation")
      self.Egalisation()
     print("Finalisation")
     self.Finalisation()

    def Division(self,mod = 2):
     aux = Tableau(self.tab.X * 2,self.tab.Y * 2)
     for y in range(self.Y):
      init = self.tab.ligne(y)
      offset = 0
      if init * 2 > y:
       offset = 1
      for x in range(init, self.X + init):
       for y2 in range(mod):
        init2 =  self.tab.ligne(y2)
        for x2 in range(init2,mod + init2):
         aux[(x)*mod+x2 - offset, y*mod+y2] = Case((x)*mod+x2 -offset,y*mod+y2)
         aux[(x)*mod+x2 - offset, y*mod+y2].biome.copy(self.tab[x,y].biome)
     self.tab = aux
     self.Y *= 2
     self.X *= 2

    def Egalisation(self):
     self.aux = Tableau(self.tab.X,self.tab.Y)
     self.tab.iter(self._egalisation)
     self.tab = self.aux

    def _egalisation(self,x,y):
     biome = self.Moyenne(x,y)
     self.aux[x,y] = Case(x,y)
     self.aux[x,y].biome = biome

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
     x1,y1 =  aux[randrange(len(aux))]
     if compteur > 0:
      for elt in biome.dict.keys():
        div = 0
        biome.div(elt,compteur)
        biome.mult(elt,self.modele.argsRand[elt]["moyenne"])
        div += self.modele.argsRand[elt]["moyenne"]
        biome.add(elt,self.tab[x,y].biome.dict[elt] * self.modele.argsRand[elt]["centre"])
        div += self.modele.argsRand[elt]["centre"]
        biome.add(elt,self.tab[x1,y1].biome.dict[elt] * self.modele.argsRand[elt]["rand"])
        div += self.modele.argsRand[elt]["rand"]
        biome.div(elt,div)
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

    def getSurface(self):
     w = sf.RenderTexture(hexagone.l * self.X + hexagone.l // 2,(hexagone.L * 1.5) * (self.Y // 2 + 1))
     w.clear()
     return w

    def getTexture(self,w):
     for elt in self.tab.values():
      w.draw(elt.sprite())
     w.display()
     return w
    
    def save(self,name):
     w = self.getTexture()
     image =  w.texture.to_image()
     image.to_file(name)
