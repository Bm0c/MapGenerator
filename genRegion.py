import sfml as sf
from tableau import Tableau
from case import Case
from random import randrange
from hexagone import hexagone

class Region:

    def __init__(self,Color,frontiere = [],interieur = []):
     self.frontiere = frontiere
     self.interieur = interieur
     self.Color = Color

    def addFro(self,case):
     self.frontiere.append(case)
     case.value = self.Color

    def addInt(self,case):
     self.interieur.append(case)
     case.value = self.Color

class GenRegion(Tableau):

    def __init__(self,largeur,hauteur, nb = 10):
     self.X = largeur
     self.Y = hauteur
     self.tab = {}
     self.regions = []
     for x,y in self.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = -1
     self.liste = [elt for elt in self.iterB() ]
     self.init = []
     for i in range(nb):
      case = self.tab[self.liste[randrange(len(self.liste))]]
      case.value = i
      self.init.append(case) 
      self.regions.append(Region(nb,interieur = [case]))
     for case in self.tab.values():
      distance = self.X * self.Y
      id = -1
      for init in self.init:
       if case.Distance(init) < distance:
        distance = case.Distance(init)
        id = init.value
      case.value = id
      voisins = [self.tab[elt] for elt in case.Voisins() if elt in self.tab and self.tab[elt].value != -1 and self.tab[elt].value != id]
      if len(voisins):
       self.regions[id].frontiere.append(case)
       for elt in voisins:
        if elt in self.regions[id].interieur:
         self.regions[id].interieur.remove(elt)
         self.regions[id].frontiere.append(elt)
      else:
       self.regions[id].interieur.append(case)
       

    def getTexture(self):
      w = sf.RenderTexture(hexagone.l * self.X + hexagone.l // 2,(hexagone.L * 1.5) * (self.Y // 2 + 1))
      w.clear()
      for region in self.regions:
        region.Color = sf.Color(randrange(256),randrange(256),randrange(256))
      for elt in self.tab.values():
       elt.biome.setColor(self.regions[elt.value].Color)
       if  elt in self.regions[elt.value].interieur:
        w.draw(elt.sprite())
      w.display()
      return w
 
    def save(self,name):
      w = self.getTexture()
      image =  w.texture.to_image()
      image.to_file(name)

def fun():
 for i in range(100):
  print("Test " + str(i))
  s = GenRegion(10,10,6)
  s.save("Test{}.png".format(i))
