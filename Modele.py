import sfml as sf
from Reader import *

class Modele:

    def __init__(self):
     self.hierarchie = [] 
     self.tab = {}
     self.pourcents = {}
     self.type = {}
    def addNode(self,name,node):
     self.tab[name] = node

    def addHierarchie(self,name):
     self.hierarchie.append(name)

    def addPourcent(self,name,liste):
     self.pourcents[name] = liste

    def determine(self,biome):
     mot = self.word(biome.dict)
     suffix = ""
     prefix, value = mot.pop(0)
     while type(self.tab[prefix,suffix][value]) != sf.Color:
      suffix = self.tab[prefix,suffix][value]
      prefix, value = mot.pop(0)
     biome.setColor(self.tab[prefix,suffix][value])

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

    def div(self,name,value):
     self.dict[name] //= value

    def copy(self,biome):
     for key,value in biome.dict.items():
      self.dict[key] = value

    def moy(self,biome):
     for key,value in biome.dict.items():
      self.dict[key] = (value + self.dict[key]) // 2

class Make(Reader):

    def __init__(self,name):
     Reader.__init__(self,name)
     self.modele = Modele()

    def makeNode(self):
     l = []
     line = self.getLine()
     while line != None and line.split(" ")[0] != "end":
      liste = line.split(":")
      if liste[1] == "COLOR":
       l.append(sf.Color(int(liste[2]),int(liste[3]),int(liste[4])))
      else:
       l.append(liste[1])
      line = self.getLine()
     return l

    def makeLayer(self,line):
     liste = line.split(":")
     name = liste[0]
     pourcents = []
     self.modele.type[name] = ""
     self.modele.addHierarchie(name)
     for elt in liste[1].split(","):
      pourcents.append(elt)
     self.modele.addPourcent(name,pourcents)
     line = self.getLine()
     while line != None and line.split(" ")[0]  != "end":
      liste = line.split(" ")
      if liste[0] == "begin":
       suffix = ""
       if len(liste) > 1:
        suffix = liste[1]
       self.modele.addNode((name,suffix),self.makeNode())
      elif "type" in line:       
       self.modele.type[name] = line.split(":")[1]
      line = self.getLine()

    def make(self):
     line = self.getLine()
     while line != None:
      liste = line.split(" ")
      if liste[0] == "def":
       self.makeLayer(liste[1])
      line = self.getLine()
