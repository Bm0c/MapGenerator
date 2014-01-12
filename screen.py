#!/usr/bin/python3
import sfml as sf
from GenMap import *
from hexagone import *

def create():
    mode = sf.VideoMode.get_desktop_mode()
    texture = sf.RenderTexture(mode.width,mode.height)
    texture.clear()
    hexagone.setl(8)
    X = (mode.width - hexagone.l // 2) // hexagone.l
    Y = int((mode.height // (hexagone.L * 1.5) - 1) * 2)
    i = 0
    while i < 4:
     X = (X // 2) + (X % 2)
     Y = (Y // 2) + (Y % 2)
     i+=1
    map = MapGen(X,Y,"LOLWUT")
    map.cycle(4)
    aff(texture,map)
    texture.texture.to_image().to_file("map.png")
    return 0

create()
