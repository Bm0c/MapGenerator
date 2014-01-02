import sfml as sf
from GenMap import *
w = sf.RenderWindow(sf.VideoMode(800,800),"LOLWUT")
w.clear()
def boucle(t,d):
 w.clear()
 while 1>0:
   a = cycle(t,d)
   aff(w,a)


