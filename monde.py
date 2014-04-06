from Modele import Modele
from genMap import MapGen
from genContinent import GenContinents
import sfml as sf
class Monde:

    def __init__(self,initX,initY,modele = "patron.xml",cycle = 2):
     self.modele = Modele(modele)
     map = MapGen(initX,initY,modele)
     print("Generating map")
     map.cycle(cycle)
     self.tab = map.tab
     print("Generating cont")
     conts = GenContinents(self.tab)
     self.continents = conts.continents

    def getTexture(self):
     w = self.tab.getSurface()
     th = lambda x,y : w.draw(self.tab[x,y].sprite())
     self.tab.iter(th)
     th = lambda x,y : w.draw(self.tab[x,y].drawRegion())
     self.tab.iter(th)
     th = lambda x,y : w.draw(self.tab[x,y].drawFrontiere())
     self.tab.iter(th)
     w.display()
     return w

    def save(self,name):
     w = self.getTexture() 
     image = w.texture.to_image()
     image.to_file(name)

