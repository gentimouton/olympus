""" background of game scene """
import pygame as pg
import pview
from pview import T

# TODO: make a bg only for the encounter area, not for the hud 
def make_bg():
    """ a static solid background. Return surface """
    surf = pg.Surface(pview.size)
    surf.fill((11, 44, 44))
    surf.fill((33, 66, 66), T(0, 0, 800, 100))
    surf.convert()
    return surf