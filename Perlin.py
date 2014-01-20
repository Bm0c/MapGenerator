import sfml as sf
import random
import math

def lineaire(a,b,x):
 return a * (1 - x) + b * x

def lineaire2D(a,b,c,d,x,y):
 return lineaire(lineaire(a,b,x),lineaire(c,d,x),y)

def cos(a,b,x):
 return lineaire(a,b,(1 - math.cos(x * math.pi))/2)
    
def cos2D(a,b,c,d,x,y):
 return cos(cos(a,b,x),cos(c,d,x),y)

class Perlin:
    
    def __init__(self,X,Y,pas,octaves):
     self.X = X
     self.Y = Y
     self.tab = {}
     self.bruit = {}
     self.pas = pas
     self.octaves = octaves
     self.octave = 0

    def randomize(self):
     self.octave = 0
     while self.octave < self.octaves:
      self.bruit[self.octave] = {}
      x = 0
      while x < self.X:
       y = 0
       while y < self.Y:
        self.bruit[self.octave][x,y] = random.random()
        y+=1
       x+=1
      self.octave += 1

    def apply(self):
     x = 0
     while x < self.X:
      y = 0
      while y < self.Y:
       if x == 0 or y == 0 or x == (self.X -1) or y == (self.Y -1):
        self.tab[x,y] = 1.0
       else:
        self.tab[x,y] = self.bruitcoherent2D(x,y,0.9)
       y+=1
      x+=1

    def getImage(self):
     image = sf.Image.create(self.X,self.Y,sf.Color.BLACK)
     for ((x,y),value) in self.tab.items():
      value = int(value * 255.0)
      image[x,y] = sf.Color(value,value,value)
     return image


    def valeur(self,x,y):
      return self.bruit[self.octave][x%self.X,y%self.Y]

    def bruit2D(self,x,y):
     i = int(x/self.pas)
     j = int(y/self.pas)
     return cos2D(self.valeur(i,j),self.valeur(i+1,j),self.valeur(i,j+1),self.valeur(i+1,j+1), \
                   (x/self.pas)%1,(y/self.pas)%1)

    def bruitcoherent2D(self,x,y,persistance):
     somme = 0
     p = 1
     self.octave = 0
     while self.octave < self.octaves :
      somme += p * self.bruit2D(x ,y)
      p *= persistance
      self.octave += 1
     return somme * (1 - persistance) / (1 - p)

def test():
 i = 0
 while i < 42:
  print(i)
  a = Perlin(30,30,5,3)
  a.randomize()
  a.apply()
  a.getImage().to_file("test{0}.png".format(i))
  i+=1
 print("---finis---")
