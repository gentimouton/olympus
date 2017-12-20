from random import randint as r

import ptext
from pview import T
import pygame as pg


def random_color():
    return r(22, 222), r(22, 222), r(22, 222)



class DebugSpr(pg.sprite.DirtySprite):
    """ Hack class to display state of the game scene on screen """ 
    def __init__(self, gs):
        pg.sprite.DirtySprite.__init__(self)
        self.layer = 100  # above everything
        self.gs = gs
        self.txt = ''
    def update(self):
        """ called every tick """
        new_txt = '--debug--\n%d encounters under' % len(self.gs.model.encounters)
        if self.txt != new_txt:
            self.txt = new_txt
            self.refresh()
    def refresh(self):
        """ re-render. called when full screening """
        self.rect = pg.Rect(T(600, 550, 200, 50))
        surf = pg.Surface(self.rect.size)
        surf.fill((255, 0, 255))
        surf.set_colorkey((255, 0, 255), pg.RLEACCEL)
        ptext.draw(self.txt, (0, 0), surf=surf, width=self.rect.w,
                   fontsize=T(16), color=(255, 255, 255),
                   antialias=False, owidth=2, ocolor=(0, 0, 0)
                   )
        surf.convert()
        self.image = surf
        self.dirty = 1
