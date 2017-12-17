""" An encounter is a situation (text, image) and choices with consequences. """
from pview import T
import pygame as pg


class Encounter():
    def __init__(self, spr_grp):
        """ spr_grp is the current scene's sprite group """
        self.txt = 'what do you do?'
        self.opt1 = 'a'
        self.opt2 = 'b'
        self.mid_card = Card((300, 150, 200, 300), (55, 55, 55), self.txt)
        self.left_card = Card((50, 150, 200, 300), (55, 55, 111), self.opt1)
        self.right_card = Card((550, 150, 200, 300), (111, 55, 55), self.opt2)
        spr_grp.add(self.mid_card, self.left_card, self.right_card)
        
        
        
class Card(pg.sprite.DirtySprite):
    def __init__(self, rect, color, txt):
        pg.sprite.DirtySprite.__init__(self)
        self.rect0 = rect
        self.color = color
        self.txt = txt
        self.refresh()
    
    def refresh(self):
        x, y, w, h = self.rect0
        inner_rect = (1, 1, T(w), T(h))
        self.rect = pg.Rect(T(x) - 1, T(y) - 1, T(w) + 2, T(h) + 2)
        surf = pg.Surface((T(w) + 2, T(h) + 2))
        surf.fill((111, 111, 55))
        surf.fill(self.color, inner_rect)
        surf.convert()
        self.image = surf
        self.dirty = 1