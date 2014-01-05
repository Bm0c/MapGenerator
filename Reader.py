class Reader:

    def __init__(self,name):
     file = open(name,"r")
     self.liste = file.read().split("\n")
     file.close()

    def getLine(self):
     if len(self.liste) > 0 : 
      return self.liste.pop(0).split("#")[0]
     else:
      return None 

