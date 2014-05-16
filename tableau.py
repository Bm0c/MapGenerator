import threading
from hexagone import hexagone
from case import Case
import sfml as sf

class Tableau:
 
     def __init__(self,largeur,hauteur):
        self.tab = {}
        self.X = largeur
        self.Y = hauteur

     def __getitem__(self,key): return self.tab[key]
     def __setitem__(self,key,value): self.tab[key] = value
     def __contains__(self,key): return key in self.tab
     def keys(self): return self.tab.keys()     
     def items(self): return self.tab.items()  
     def values(self): return self.tab.values()

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
 
     def iterTh(self,fun):
        Ths = []
        for i in range(2):
            for j in range(2):
                Ths.append(threading.Thread(None,self.iterHalf,None,(i * (self.X // 2 ),j * (self.Y // 2), fun),None))
        for th in Ths: th.start()
        while threading.activeCount() > 1: pass

     def iterHalf(self,offsetX,offsetY,fun):
        for y in range(offsetY,offsetY + self.Y//2):
            init = self.ligne(y)
            for x in range(init + offsetX,offsetX + self.X // 2 + init):
                fun(x,y)

     def iter(self,fun):
        for y in range(self.Y):
            init = self.ligne(y)
            for x in range(init,self.X + init):
                fun(x,y) 

     def save(self,name):
        w = self.getTexture()
        image = w.texture.to_image()
        image.to_file(name)

     def getSurface(self):
        w = sf.RenderTexture(hexagone.l * self.X + hexagone.l // 2,(hexagone.L * 1.5) * (self.Y // 2 + 1))
        w.clear()
        return w

