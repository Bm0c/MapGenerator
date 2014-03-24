import sfml as sf
from Reader import *
import lecteur

class Modele:

    def __init__(self,file):
     fichier = lecteur.Lecteur(file)
     fichier.parse()
     self.racine = fichier.racine
     self.hierarchie = self.racine["liste"] 
     self.tab = {}
     self.pourcents = {}
     for key,elt in self.racine["couche"].items():
      self.pourcents[key] = [int(value) for value in elt["pourcents"] ]

    def determine(self,biome):
     mot = self.word(biome.dict)
     suffix = "init"
     prefix, value = mot.pop(0)
     Couleur = self.racine["couche"][prefix]["variation"][suffix]["niveau"][value]
     while type(Couleur) != sf.Color and not "def" in Couleur:
      suffix = Couleur
      prefix, value = mot.pop(0)
      Couleur = self.racine["couche"][prefix]["variation"][suffix]["niveau"][value]
     biome.walkable = not  "walkable" in self.racine["def"][Couleur]
     if type(Couleur) != sf.Color:
      Couleur = self.racine["def"][Couleur]["color"]
     biome.setColor(Couleur)

    def word(self,dict):
     l = []
     for elt in self.hierarchie :
      l.append((elt,dict[elt]))
     return l

class Biome:
    
    def __init__(self):
     self.dict = {} 
     self.color = sf.Color.WHITE

    def setColor(self,color):
     self.color = color

    def add(self,name,value):
     self.dict[name] += value

    def set(self,name,value):
     self.dict[name] = value

    def mult(self,name,value):
     self.dict[name] *= value

    def div(self,name,value):
     self.dict[name] //= value

    def copy(self,biome):
     for key,value in biome.dict.items():
      self.dict[key] = value

    def moyBiome(self,biome):
     for key,value in biome.dict.items():
      self.add(key,value)
      self.div(key,2)

    def addBiome(self,biome):
     for key,value in biome.dict.items():
      self.add(key,value)
