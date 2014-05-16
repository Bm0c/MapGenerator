import sfml as sf
from hexagone import *
from Modele import Biome

class Case(hexagone):

    def __init__(self,u,v,region = None,continent = False):
        self.u = u
        self.v = v
        self.biome = Biome()
        self.region = region
        self.continent = continent
        self.frontiere = []

    def _hexa(self):
        h = sf.CircleShape(self.L/2,6)
        h.position = self.getXY()
        h.fill_color = sf.Color.BLACK
        return h

    def sprite(self):
        h = self._hexa()
        h.fill_color = self.biome.color
        h.outline_color = sf.Color(0,0,0,40)
        h.outline_thickness = -1
        return h

    def drawRegion(self):
        h = self._hexa()
        if self.region:
            h.fill_color = self.region.Color
        else :
            h.fill_color = sf.Color(0,0,0,0)
        return h

    def drawFrontiere(self):
        lines = sf.VertexArray(sf.PrimitiveType.LINES)
        if self.region != None:
            h = self._hexa()
            for i in self.frontiere:
                v1 = sf.Vertex()
                v1.color = sf.Color.BLACK#self.region.Color
                v1.position = h.get_point(i) + h.position
                v2 = sf.Vertex()
                v2.color = sf.Color.BLACK#self.region.Color
                v1.position = h.get_point(i) + h.position
                v2.position = h.get_point((i + 1) % 6) + h.position
                lines.append(v1)
                lines.append(v2)
        return lines

    def setRegion(self,region):
        self.region = region

    def setFrontiere(self,tab):
        self.frontiere = [ i for i,elt in enumerate(self.Voisins()) if ( elt in tab and self.region != tab[elt].region ) or ( not elt in tab ) ]
