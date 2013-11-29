from random import randrange
from case import Case

class MapGen:
        
    def __init__(self,largeur,hauteur,coeff): #X,Y,Liste_Coeff
        self.X = largeur
        self.Y = hauteur
        self.listeCoeff = coeff
        self.MAXVALUE = 250
        self.tab = {}

    def matriceRandom(self):
        y = 0
        while y < self.Y:
            x = 0
            while x < self.X:
                self.tab[x,y]= Case(x,y,randrange(self.MAXVALUE))
                x += 1
            y += 1

    def cycle(self,duree):
        while duree > 0:
            duree -= 1
            self.Division()
            self.Egalisation()
        self.Finalisation()
        

    def Division(self,mod = 2):
        aux = {}
        y = 0
        while y < self.Y:
            x = 0
            while x < self.X:
                y2 = 0
                while y2 < mod:
                    x2 = 0
                    while x2 < mod:
                      aux[x*mod+x2, y*mod+y2] = Case(x*mod+x2,y*mod+y2,self.tab[x,y].couleur)
                      x2 += 1
                    y2 += 1
                x += 1
            y += 1
        self.tab = aux
        self.Y *= 2
        self.X *= 2

    def Egalisation(self):
        aux = {}
        y = 0
        while y < self.Y:
           x = 0
           while x < self.X:
            aux[x,y] = Case(x,y,self.Moyenne(x,y))
            x += 1
           y += 1
        self.tab = aux

    def Moyenne(self,x,y):
       aux = []
       moyenne = 0
       compteur = 0
       for elt in self.tab[x,y].Voisins():
         x1,y1 = elt
         try:
          moyenne = moyenne + self.tab[x1,y1].couleur
          compteur = compteur + 1
          aux.append(elt)
         except:
          a = 42
       moyenne = moyenne // compteur
       x1,y1 =  aux[randrange(compteur)]
       moyenne = moyenne + self.tab[x1,y1].couleur
       return moyenne // 2

    def Finalisation(self):
        aux = {}
        self.niveaux = []
        i = 0
        while i < self.MAXVALUE:
            aux[i] = 0
            i += 1
        y = 0
        while y < self.Y:
            x = 0
            while x < self.X:
                aux[self.tab[x,y].couleur] += 1
                x += 1
            y +=1
        buffer_ = 1
        i = 0
        for elt in self.listeCoeff:
            while(i < self.MAXVALUE and buffer_*100/(self.X*self.Y) < elt):
                buffer_ += aux[i]
                i+=1
            self.niveaux.append(i)
        print(self.niveaux)
        #for elt in aux.values():
        #    print (elt)

def aff(w,Poney):
 for elt in Poney.tab.values():
  w.draw(elt.sprite())
 w.display()
def cycle(t): 
 Poney1 = MapGen(4,4,[20,56,70,100])
 Poney1.matriceRandom()
 Poney1.cycle(t)
 
 Poney2 = MapGen(4,4,[20,56,70,100])
 Poney2.matriceRandom()
 Poney2.cycle(t)
 
 Poney3 = MapGen(4,4,[20,56,70,100])
 Poney3.matriceRandom()
 Poney3.cycle(t)
 
 Poney = MapGen(Poney3.X,Poney3.Y,[])
 Poney.matriceRandom()
 x = 0
 while x < Poney3.X:
  y = 0
  while y < Poney3.Y:
   Poney.tab[x,y].r = Poney1.tab[x,y].couleur
   Poney.tab[x,y].g = Poney2.tab[x,y].couleur
   Poney.tab[x,y].b = Poney3.tab[x,y].couleur
   y = y + 1
  x = x + 1
 return Poney

