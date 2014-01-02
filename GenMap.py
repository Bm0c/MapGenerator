from random import randrange
from case import Case

class MapGen:
        
    def __init__(self,largeur,hauteur,coeff): #X,Y,Liste_Coeff
        self.X = largeur
        self.Y = hauteur
        self.listeCoeff = coeff
        self.MAXVALUE = 255
        self.tab = {}

    def ligne (self,y): 
        return (y+1)//2


    def matriceRandom(self):
        y = 0
        while y < self.Y:
            init = self.ligne(y)
            x = init
            while x < self.X + init:
                self.tab[x,y]= Case(x,y,randrange(self.MAXVALUE),randrange(self.MAXVALUE),randrange(self.MAXVALUE))
                x += 1
            y += 1

    def cycle(self,duree):
        while duree > 0:
            duree -= 1
            self.Division()
            self.Egalisation()
        

    def Division(self,mod = 2):
        aux = {}
        y = 0
        while y < self.Y:
            init = self.ligne(y)
            x = init
            offset = 0
            if x * 2 > y:
                offset = 1
            while x < self.X + init:
                y2 = 0
                while y2 < mod:
                    init2 =  self.ligne(y2)
                    x2 = init2
                    while x2 < mod + init2:
                      aux[(x)*mod+x2 - offset, y*mod+y2] = Case((x)*mod+x2 -offset,y*mod+y2,self.tab[x,y].r,self.tab[x,y].b,self.tab[x,y].g)
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
           init = self.ligne(y)
           x = init
           while x < self.X + init:
            (r,b,g) = self.Moyenne(x,y)
            aux[x,y] = Case(x,y,r,b,g)
            x += 1
           y += 1
        self.tab = aux

    def Moyenne(self,x,y):
       aux = []
       moyenne_r = 0
       moyenne_b = 0
       moyenne_g = 0
       compteur = 0
       for elt in self.tab[x,y].Voisins():
         x1,y1 = elt
         try:
          moyenne_r = moyenne_r + self.tab[x1,y1].r
          moyenne_b = moyenne_b + self.tab[x1,y1].b
          moyenne_g = moyenne_g + self.tab[x1,y1].g
          aux.append(elt)
          compteur = compteur + 1
         except:
          a = 42
       moyenne_r = moyenne_r // compteur
       moyenne_b = moyenne_b // compteur
       moyenne_g = moyenne_g // compteur
       x1,y1 =  aux[randrange(compteur)]
       moyenne_r = moyenne_r + self.tab[x1,y1].r
       moyenne_b = moyenne_b + self.tab[x1,y1].b
       moyenne_g = moyenne_g + self.tab[x1,y1].g

       return (moyenne_r // 2,moyenne_b // 2,moyenne_g // 2)

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
def cycle(t,d): 
 Poney = MapGen(d,d,[])
 Poney.matriceRandom()
 Poney.cycle(t)
 i = 0
 return Poney
