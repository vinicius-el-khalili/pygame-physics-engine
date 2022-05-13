import pygame as pg
import random
from math import *
# Settings #
title = 'Stuffy stuffs'
tilesize = 20
xtiles = 60
ytiles = 30

width = tilesize*xtiles
height = tilesize*ytiles
fps = 80
gravity = .05
#COLORS
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
purple = (40, 16, 68)
randcolors = [pg.Color('#ffe2e2'),pg.Color('#7579e7'),pg.Color('#ff9a76'),pg.Color('#f0a500'),
              pg.Color('#d6e0f0'),pg.Color('#206a5d')]
vec = pg.math.Vector2