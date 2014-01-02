import sfml as sf
from hexagone import *

class Case(hexagone):

    def __init__(self,u,v,r,b,g):
         self.u = u
         self.v = v
         self.r = r
         self.b = b
         self.g = g

    def sprite(self):
         h = sf.CircleShape(self.L/2,6)
         h.position = self.getXY()
         h.fill_color = sf.Color(self.r,self.b,self.g)
         return h


