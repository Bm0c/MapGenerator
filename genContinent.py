from continent import Continent
from tableau import Tableau
from genRegion import GenRegionPasse
from random import randrange
import sfml as sf 

class GenContinents(Tableau):

    def __init__(self,tab,largeur,hauteur):
     self.X = largeur
     self.Y = hauteur
     self.hauteur = hauteur
     self.tab = tab
     self.continents = []
     self.iter(self._makeContinent)

    def getTexture(self,w):
     for cont in self.continents:
      for region in cont.regions:
        region.Color = sf.Color(randrange(256),randrange(256),randrange(256),80)
     th = lambda x,y : w.draw(self.tab[x,y].sprite())
     self.iter(th) 
     th = lambda x,y : w.draw(self.tab[x,y].drawFrontiere())
     self.iter(th)
     w.display()

    def _makeContinent(self,x,y):
     if not ( self.tab[x,y].biome.walkable and self.tab[x,y].region == None ):
      return
     cases = [ (x,y) ]
     self.tab[x,y].continent = True
     voisins = self.tab[x,y].Voisins()
     while len(voisins):
      elt  = voisins.pop(0)
      if elt in self.tab and self.tab[elt].biome.walkable and not self.tab[elt].continent:
       self.tab[elt].continent = True
       cases.append(elt)
       voisins.extend(self.tab[elt].Voisins())
     regions = GenRegionPasse(self.tab,cases,self.X,self.Y,3)
     regions.finalisation
     print(regions.liste)
     self.continents.append(Continent(regions.liste))
