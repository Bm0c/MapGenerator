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
     case.region = self

    def addInt(self,case):
     self.interieur.append(case)
     case.region = self

class GenRegion(Tableau):

    def __init__(self,largeur,hauteur, nb = 10):
     self.X = largeur
     self.Y = hauteur
     self.regions = []
     for x,y in self.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = -1
       

    def getTexture(self):
      w = sf.RenderTexture(hexagone.l * self.X + hexagone.l // 2,(hexagone.L * 1.5) * (self.Y // 2 + 1))
      w.clear()
      for region in self.regions:
       region.Color = sf.Color(randrange(256),randrange(256),randrange(256),255)
      for elt in self.tab.values():
       elt.setFrontiere(self.tab)
       w.draw(elt.drawRegion())
      w.display()
      return w
 
    def save(self,name):
      w = self.getTexture()
      image =  w.texture.to_image()
      image.to_file(name)

class GenRegionVoronoi(GenRegion,Tableau):

    def __init__(self,largeur,hauteur, nb = 10):
     self.tab = {}
     GenRegion.__init__(self,largeur,hauteur,nb)
     self.init = []
     self.liste = [elt for elt in self.iterB() ]
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
       self.regions[id].addFro(case)
       for elt in voisins:
        if elt in self.regions[id].interieur:
         self.regions[id].interieur.remove(elt)
         self.regions[id].addFro(elt)
      else:
       self.regions[id].addInt(case)


class GenRegionPasse(GenRegion):

    def __init__(self,tab,liste,largeur,hauteur,nb = 10, passe = 5):
     self.tab = {}
     GenRegion.__init__(self,largeur,hauteur,nb)
     self.tab = tab
     self.liste = liste
     for i in range(nb):
      case = self.tab[self.liste[randrange(len(self.liste))]]
      case.value = i
      self.regions.append(Region(nb,frontiere = [case]))
     changement = True
     while len(liste) and changement:
      changement = False
      for region in self.regions:
       voisins = []
       for elt in region.frontiere:
        v = [ key for key in elt.Voisins() if key in liste ]
        if len(v):
         voisins += v
        else :
         region.frontiere.remove(elt)
         region.interieur.append(elt)
       i = 0
       while len(voisins) and len (liste) and i < passe :
        changement = True
        x,y = voisins[randrange(len(voisins))]
        while(x,y) in voisins:
         voisins.remove((x,y))
        liste.remove((x,y))
        region.addFro(self.tab[x,y])
        i += 1

    def getTexture(self):
      w = sf.RenderTexture(hexagone.l * self.X + hexagone.l // 2,(hexagone.L * 1.5) * (self.Y // 2 + 1))
      w.clear()
      for region in self.regions:
       region.Color = sf.Color(randrange(256),randrange(256),randrange(256),80)
      for elt in self.tab.values():
       w.draw(elt.sprite())
      for elt in self.tab.values():
       elt.setFrontiere(self.tab)
       w.draw(elt.drawRegion())
       w.draw(elt.drawFrontiere())
      w.display()
      return w
