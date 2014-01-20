import sfml as sf
from GenMap import *
from hexagone import *
w = sf.RenderTexture(1158,1000)#hexagone.l * X + hexagone.l * 0.5 / (hexagone.L * 1.5) *( Y / 2)
w.clear()
def boucle(t,d):
 w = sf.RenderWindow(sf.VideoMode(1,1),"LOLWUT")
 w.clear()
 while 1>0:
  a = cycle(t,d)
  aff(w,a)
  print(a.X)
  print(a.Y)

def Generate(t,d,n):
 w = sf.RenderTexture(1,1)
 w.clear()
 i = 0
 while i < n:
  print("Working on {0}...".format(i))
  a = cycle(t,d)
  w = sf.RenderTexture(hexagone.l * a.X + hexagone.l // 2,(hexagone.L * 1.5) * (a.Y // 2 + 1))#hexagone.l * X + hexagone.l * 0.5 / (hexagone.L * 1.5) *( Y / 2)
  w.clear()
  aff(w,a)
  image = w.texture.to_image()
  image.to_file("map{0}.png".format(i))
  i+=1

def test():
 tab = {}
 i = 0
 while i < 42:
  tab[i] = sf.Image.from_file("test{0}.png".format(i))
  i += 1
 i = 0
 while i < 21:
  print(i)
  a = MapGen(30,30,"patron")
  a.fromImage(tab[i*2],"Relief")
  a.fromImage(tab[i*2+1],"Vegetation")
  j = 0
  while j < 3:
   a.Division()
   a.Egalisation()
   j += 1
  a.Finalisation()
  i += 1
  w = sf.RenderTexture(hexagone.l * a.X + hexagone.l // 2,(hexagone.L * 1.5) * (a.Y // 2 + 1))
  w.clear()
  aff(w,a)
  image = w.texture.to_image()
  image.to_file("map{0}.png".format(i))
  i += 1

