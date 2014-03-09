import sfml as sf
from hexagone import *
from Modele import Biome

class Case(hexagone):

    def __init__(self,u,v):
     self.u = u
     self.v = v
     self.biome = Biome()

    def sprite(self):
     h = sf.CircleShape(self.L/2,6)
     h.position = self.getXY()
     h.fill_color = self.biome.color
     h.outline_color = sf.Color(0,0,0,40)
     h.outline_thickness = -1
     return h


