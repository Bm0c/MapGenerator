import sfml as sf
from tableau import Tableau
from case import Case
from random import randrange
from hexagone import hexagone
from region import Region

class GenRegion:

    def __init__(self, nb = 10):
     self.regions = []

    def getSurface(self):
      w = sf.RenderTexture(hexagone.l * self.X + hexagone.l // 2,(hexagone.L * 1.5) * (self.Y // 2 + 1))
      w.clear()
      return w

    def getTexture(self,w):
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

class GenRegionVoronoi(GenRegion):

    def __init__(self,largeur,hauteur, nb = 10):
     GenRegion.__init__(self,nb)
     self.tab = Tableau(largeur,hauteur)
     for x,y in self.tab.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = -1
     self.init = []
     self.liste = [elt for elt in self.tab.iterB() ]
     for i in range(nb):
      case = self.tab[self.liste[randrange(len(self.liste))]]
      case.value = i
      self.init.append(case) 
      self.regions.append(Region(nb,interieur = [case]))
     for case in self.tab.values():
      distance = self.tab.X * self.tab.Y
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

    def __init__(self,tab,liste = None ,nb = 10, passe = 20):
     GenRegion.__init__(self,nb)
     self.tab = tab
     if liste == None:
      self.liste = list(tab.tab)
     else:
      self.liste = liste
     for i in range(nb):
      case = self.tab[self.liste[randrange(len(self.liste))]]
      case.value = i
      self.regions.append(Region(nb,interieur = [case]))
      self.regions[i].voisins =  [ key for key in case.Voisins() if key in self.liste ]
     changement = True
     while changement:
      changement = not changement
      for region in self.regions:
       i = 0
       while len(region.voisins) and i < passe :
        x,y = region.voisins.pop(randrange(len(region.voisins)))
        if tab[x,y].region == None :
         changement = True
         self.liste.remove((x,y))
         region.voisins.extend([elt for elt in tab[x,y].Voisins() if elt in tab and tab[elt].biome.walkable])
         i += 1
         region.addInt(tab[x,y])

    def finalisation(self):
      print("Finalisation")
      for region in self.regions:
       region.Color = sf.Color(randrange(256),randrange(256),randrange(256),80)
       inte,frot = [],[]
       for elt in region.interieur:
        elt.setFrontiere(self.tab)
        if len(elt.frontiere):
         frot.append(elt)
        else:
         inte.append(elt)
       region.interieur = inte
       region.frontieres = frot

    def getTexture(self,w):
      th = lambda x,y : w.draw(self.tab[x,y].sprite())
      self.tab.iter(th)
      th = lambda x,y : w.draw(self.tab[x,y].drawFrontiere())
      self.tab.iter(th)
      w.display()
      return w
