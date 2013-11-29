import sfml as sf
from hexagone import *

class Case(hexagone):

	def __init__(self,u,v,couleur):
	 self.u = u
	 self.v = v
	 self.r = 0
	 self.b = 0
	 self.couleur = couleur
	 self.g = 0
	def sprite(self):
	 h = sf.CircleShape(self.L/2,6)
	 h.position = self.getXY()
	 h.fill_color = sf.Color(self.r,self.g,self.b)
	 return h


def tab():
	tab = {} 
	i = 10
	while i < 30:
	 j = 1 
	 while j < 15:
	  tab[i,j] = Case(i,j,sf.Color.RED)
	  j = j + 1
	 i = i + 1
	return tab

tab()
