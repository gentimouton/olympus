""" background of game scene """
import pygame as pg
import pview
from pview import T
from utils import random_color

# TODO: make a bg only for the encounter area, not for the hud
# TODO: bg = mountain with drifting clouds, or city when disguised as human
_bgcol1 = random_color()
_bgcol2 = random_color()  
def make_bg():
    """ a static solid background. Return surface """
    surf = pg.Surface(pview.size)
    surf.fill(_bgcol1)
    surf.fill(_bgcol2, T(0, 0, 800, 100))
    surf.convert()
    return surf