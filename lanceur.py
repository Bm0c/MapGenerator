import sfml as sf
from GenMap import *
w = sf.RenderWindow(sf.VideoMode(1160,1000),"LOLWUT")
w.clear()
def boucle(t,d):
 w.clear()
 while 1>0:
  a = cycle(t,d)
  aff(w,a)
  print(a.X)
  print(a.Y)

def Generate(t,d,n):
 w.clear()
 i = 0
 while i < n:
  print("Working on {0}...".format(i))
  w.clear()
  a = cycle(t,d)
  aff(w,a)
  image = w.capture()
  image.to_file("{0}.png".format(i))
  i+=1
