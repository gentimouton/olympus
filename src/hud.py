""" heads up display. bunch of gauges and icons and text. """
from pview import T
import pygame as pg


# TODO: take care of hud bg in here, not in game_bg

class Hud():
    def __init__(self, spr_grp, state):
        # TODO: pass a rect saying where the HUD lives
        self.state = state
        v, vmax = state['mana']['v'], state['mana']['vmax']
        self.gauge = Gauge(v, vmax, (100, 5, 20, 70))
        self.icon = ManaIcon((100 + 2, 80, 16, 16))
        spr_grp.add(self.gauge, self.icon)

class ManaIcon(pg.sprite.DirtySprite):
    """ static icon. Square with a hole in the middle. """
    def __init__(self, rect0):
        pg.sprite.DirtySprite.__init__(self)
        self.rect0 = rect0
        self.refresh()
    def refresh(self):
        x, y, w, h = self.rect0
        self.rect = pg.Rect(T(x), T(y), T(w), T(h))
        surf = pg.Surface((T(w), T(h)))
        surf.fill((255, 0, 0))
        hole = T(w // 4), T(h // 4), T(w // 2), T(h // 2) 
        surf.fill((255, 0, 255), hole)
        surf.set_colorkey((255, 0, 255), pg.RLEACCEL)
        surf.convert()
        self.image = surf
        self.dirty = 1
        
class Gauge(pg.sprite.DirtySprite):
    def __init__(self, v, vmax, rect0, color=(222, 22, 22), bgcolor=(0, 0, 0)):
        pg.sprite.DirtySprite.__init__(self)
        self.v = v
        self.vmax = vmax
        self.rect0 = rect0
        self.color = color
        self.bgcol = bgcolor
        self.refresh()
        
    def refresh(self):
        # draw gauge itself
        b = 2  # border thickness, in px, fixed across resolutions
        # TODO: change this border from outward margin to inward padding
        x, y, w, h = self.rect0
        self.rect = pg.Rect((T(x) - b, T(y) - b, T(w) + 2 * b, T(h) + 2 * b))
        surf = pg.Surface((self.rect.w, self.rect.h))
        surf.fill(self.bgcol)  # empty part
        if self.v > 0:  # full part
            fh = h * self.v // self.vmax  # height of full part   
            inner_rect = pg.Rect(b, T(h - fh) + b, T(w), T(fh))
            surf.fill(self.color, inner_rect)
        surf.convert()
        self.image = surf
        self.dirty = 1
        