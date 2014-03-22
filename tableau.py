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
