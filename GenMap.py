from random import randrange,randint
from case import Case
from Modele import *
from hexagone import *
from tableau import Tableau
from genRegion import GenRegion

class Tableau:

    def ligne(self,y):
     return (y + 1) // 2
    
    def iterB(self,decalage = 1):
     for y in range(self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       if (x  >= init + decalage and  y >= decalage and  y < self.Y - decalage and x < self.X + init - decalage):
         yield (x,y)

    def iterC(self):
     for y in range(self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
        yield (x,y)

    def iter(self,tab):
     for y in range(self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
        yield (x,y,tab[x,y])

class Region(Tableau):

    def __init__(self,largeur,hauteur,nb = 10):
     self.X = largeur
     self.Y = hauteur
     self.tab  = {}
     self.reg= []
     self.liste = [ elt for elt in self.iterC() ]
     for x,y in self.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].biome.color = sf.Color.WHITE
     for i in range(nb):
      elt = self.liste[randrange(len(self.liste))]
      self.reg.append((elt,sf.Color(randrange(256),randrange(256),randrange(256))))
     for key,elt in self.tab.items():
      distance = self.X * self.Y
      c = sf.Color.BLACK
      for init,color in self.reg:
       if elt.Distance(self.tab[init]) < distance:
        c = color
        distance = elt.Distance(self.tab[init])
      elt.biome.color = c
       

    def getTexture(self):
     w = sf.RenderTexture(hexagone.l * self.X + hexagone.l // 2,(hexagone.L * 1.5) * (self.Y // 2 + 1))
     w.clear()
     for elt in self.tab.values():
      w.draw(elt.sprite())
     w.display()
     return w

    def save(self,name):
     w = self.getTexture()
     image =  w.texture.to_image()
     image.to_file(name)
       



class Seed(Tableau):

    def __init__(self,largeur,hauteur,noeud = {"type" : "plaque"},minValue = 0,maxValue = 255, value = 0):
     self.function = {"rand" : self.rand, "degrade" : self.degrade, "islande" : self.islande ,"plaque" : self.plaque}
     self.maxValue = maxValue
     self.minValue = minValue
     self.X = largeur
     self.Y = hauteur
     self.tab = {}
     if "args" in noeud:
      self.function[noeud["type"]](noeud["args"])
     else :
      self.function[noeud["type"]]()

    def degrade(self,args = {"direction":"Y","evolution":"increase"}):
     if args["direction"] == "Y":
      c = self.Y
      current = lambda x,y : y
     else:
      c =  self.X 
      current = lambda x,y : x - self.ligne(y) 
     if args["evolution"] == "increase":
      fun = lambda x,y : self.maxValue * current(x,y) // c
     elif args["evolution"] == "decrease":
      fun = lambda x,y : self.maxValue * (c - (1 + current(x,y))) // c
     elif args["evolution"] == "center":
      fun = lambda x,y : min(self.maxValue * current(x,y) // c,self.maxValue * (c - (1 + current(x,y))) //c) * 2
     elif args["evolution"] == "border":
      fun = lambda x,y : max(self.maxValue * current(x,y) // c,self.maxValue * (c - (1 + current(x,y))) //c) - ( self.maxValue // 2) * 2
     for(x,y) in self.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = fun(x,y) 

    def rand(self,args = {}):
     for(x,y) in self.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = randint(self.minValue,self.maxValue) 

    def islande(self,args = (2,[100,95,80,60,0])):
     for x,y in self.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = self.minValue 
     liste = [ elt for elt in self.iterB() ]
     le = len(liste)
     nb , li = args
     sup = li[0] 
     inf = li[1]
     aux = []
     for i in range(nb):
      l = [ elt for elt in self.iterB(1) ]
      elt = l[randrange(len(l))]
      self.tab[elt].value = randint(inf  * self.maxValue  // 100, sup * self.maxValue // 100)
      aux = aux + [ v for v in self.tab[elt].Voisins() if v in liste  ]
      if elt in liste:
       liste.remove(elt)
      l.remove(elt)
     current = nb
     for inf_ in li[2:]:
      sup = inf
      inf = inf_ 
      for i in range((sup - inf)  * le // 100) :
       for y in range(10):
        current = aux[randrange(len(aux))]
        aux.remove(current)
        if current in liste:
         liste.remove(current)
         self.tab[current].value = randint(inf *  self.maxValue //100,sup * self.maxValue // 100) 
         aux = aux + [ elt for elt in self.tab[current].Voisins() if elt in liste  ]
         break

    def plaque(self,args = {"nombre" : 5, "plaques" : 8}):
     for x,y in self.iterC():
      self.tab[x,y] = Case(x,y)
      self.tab[x,y].value = 0 #randrange(self.minValue , (self.minValue + self.maxValue // 2) )
     liste = [ elt for elt in self.iterB(2) ]
     nombre = int(args["nombre"])
     plaque = int(args["plaques"])
     plaques = GenRegion(self.X,self.Y, nb = plaque)
     liste_plaque = [ (elt.interieur,elt.frontiere) for elt in plaques.regions]
     for i in range(nombre):
      li,lf = liste_plaque[randrange(len(liste_plaque))]
      liste_plaque.remove((li,lf))
      l = [ (elt.u,elt.v)  for elt in li if (elt.u,elt.v) in liste]
      for elt in l:
       self.tab[elt].value = randint((self.minValue + self.maxValue)  // 2 , self.maxValue )

    def getTexture(self):
     w = sf.RenderTexture(hexagone.l * self.X + hexagone.l // 2,(hexagone.L * 1.5) * (self.Y // 2 + 1))
     w.clear()
     for elt in self.tab.values():
      elt.biome.setColor(sf.Color(elt.value,elt.value,elt.value))
      w.draw(elt.sprite())
     w.display()
     return w

    def save(self,name):
     w = self.getTexture()
     image =  w.texture.to_image()
     image.to_file(name)

class MapGen(Tableau):

    def __init__(self,largeur,hauteur,modele): #X,Y,Liste_Coeff
     self.X = largeur
     self.Y = hauteur
     self.MAXVALUE = 256
     self.tab = {}
     self.modele = Modele("patron.xml")
     self.seed = [ (key, Seed(self.X,self.Y,elt["seed"])) for key,elt in self.modele.racine["couche"].items() ]
     for x,y in self.iterC():
      self.tab[x,y] = Case(x,y)
      for key,s in self.seed:
       self.tab[x,y].biome.set(key,s.tab[x,y].value)

    def cycle(self,duree):
     for i in range(duree):
      self.Division()
      self.Egalisation()
     self.Finalisation()

    def Division(self,mod = 2):
     aux = {}
     for y in range(self.Y):
      init = self.ligne(y)
      offset = 0
      if init * 2 > y:
       offset = 1
      for x in range(init, self.X + init):
       for y2 in range(mod):
        init2 =  self.ligne(y2)
        for x2 in range(init2,mod + init2):
         aux[(x)*mod+x2 - offset, y*mod+y2] = Case((x)*mod+x2 -offset,y*mod+y2)
         aux[(x)*mod+x2 - offset, y*mod+y2].biome.copy(self.tab[x,y].biome)
     self.tab = aux
     self.Y *= 2
     self.X *= 2

    def Egalisation(self):
     aux = {}
     for y in range(self.Y):
      init = self.ligne(y)
      for x in range(init,self.X + init):
       biome = self.Moyenne(x,y)
       aux[x,y] = Case(x,y)
       aux[x,y].biome = biome
     self.tab = aux


    def Moyenne(self,x,y):
     aux = []
     biome = Biome()
     compteur = 0
     for elt in self.modele.hierarchie:
      biome.set(elt,0)
     for elt in self.tab[x,y].Voisins():
      if elt in self.tab: 
       for elt1 in self.modele.hierarchie:
        biome.add(elt1,self.tab[elt].biome.dict[elt1])
       aux.append(elt)
      compteur = compteur + 1
     x1,y1 =  aux[randrange(len(aux))]
     if compteur > 0:
      for elt in biome.dict.keys():
        biome.div(elt,compteur)
        biome.add(elt,self.tab[x,y].biome.dict[elt])
        biome.add(elt,self.tab[x1,y1].biome.dict[elt])
        biome.div(elt,3)
     return biome

    def Finalisation(self):
     aux = {}
     self.niveaux = {}
     for i in range(self.MAXVALUE):
      for elt in self.modele.hierarchie:
       aux[elt,i] = 0
     for case in self.tab.values():
      for elt in self.modele.hierarchie:
       aux[elt,case.biome.dict[elt]] += 1
     for elt in self.modele.hierarchie:
      self.niveaux[elt] = []
      i = 0
      buffer_ = 1
      for valeur in self.modele.pourcents[elt]:
       valeur = float(valeur)
       while(i < self.MAXVALUE and buffer_*100/(self.X*self.Y) <= valeur):
        buffer_ += aux[elt,i]
        i+=1
       self.niveaux[elt].append(i)
     for case in self.tab.values():
      for elt in self.modele.hierarchie:
       i = 0
       while i < len(self.niveaux[elt]) and case.biome.dict[elt] > self.niveaux[elt][i]:
        i += 1
       case.biome.dict[elt] = i
      self.modele.determine(case.biome)

    def getTexture(self):
     w = sf.RenderTexture(hexagone.l * self.X + hexagone.l // 2,(hexagone.L * 1.5) * (self.Y // 2 + 1))
     w.clear()
     for elt in self.tab.values():
      w.draw(elt.sprite())
     w.display()
     return w
    
    def save(self,name):
     w = self.getTexture()
     image =  w.texture.to_image()
     image.to_file(name)
    
    def addMap(self,map,i,j):
     i = i + self.ligne(j)
     for x,y in map.tab.keys():
      self.tab[i + x ,y+j].biome.addBiome(map.tab[x,y].biome)

    def moyMap(self,map,i,j):
     i = i + self.ligne(j)
     for x,y in map.tab.keys():
      self.tab[i + x ,y+j].biome.moyBiome(map.tab[x,y].biome)

def GenerateMap(n,x,y):
 map = MapGen(x,y,42)
 map.cycle(n)
 return map

def fun():
 for i in range(100):
  print("Test " + str(i))
  s = Seed(10,10)
  s.save("Test{}.png".format(i))
