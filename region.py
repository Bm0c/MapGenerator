class Region:

    def __init__(self,Color,frontiere = [],interieur = [],continent = None):
     self.frontiere = []
     self.interieur = interieur
     self.Color = Color
     self.continent = continent

    def addFro(self,case):
     self.frontiere.append(case)
     case.region = self

    def addInt(self,case):
     self.interieur.append(case)
     case.region = self

