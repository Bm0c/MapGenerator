import math
class hexagone:
	
    l = 8
    L = (2 * l) / (math.sqrt(3))

    def __init__(self,u,v):
     self.u = u
     self.v = v

    def Distance(self,cible):
     du = self.u - cible.u 
     dv = self.v - cible.v
     d6 = int ((abs(du) + abs(dv) + abs(du - dv)) / 2)
     return d6

    def Voisins(self):
     return [(self.u + 1,self.v),(self.u + 1,self.v + 1),(self.u,self.v+1),(self.u -1,self.v),(self.u -1,self.v - 1),(self.u,self.v - 1)]

    def getXY(self):
     x = hexagone.l * self.u - (hexagone.l/2) * self.v
     y = (3 * hexagone.L / 4) * self.v
     return x,y
