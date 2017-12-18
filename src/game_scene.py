""" The game scene has a HUD with gauges and a series of encounters. 
Player makes decisions during encounters, affecting gauges. 
Game is over when certain gauges reach certain states.
"""
from controls import controller
from encounter import Encounter
import ptext
from pview import T
import pview
import pygame as pg
from scene import SCN_MENU, Scene


class GameScene(Scene):        
    def __init__(self):
        # model
        self.mana = 10
        self.mana_max = 100
        # gfx
        self.bg = _make_bg()
        self.sprites = pg.sprite.LayeredDirty()
        self.encounters = [Encounter(self.sprites)]
        self.mana_gauge_v = Gauge(self.mana, self.mana_max, (100, 5, 20, 70)) 
        self.sprites.add(self.mana_gauge_v)
        
    def tick(self, ms):
        if controller.btn_event('select'):
            return SCN_MENU, {}
        self._render()
        return None, {}
    
    def reset_resume(self):
        self.refresh_view()
        
    def refresh_view(self):
        self.bg = _make_bg()
        pview.screen.blit(self.bg, (0, 0))
        for spr in self.sprites:
            spr.refresh()
        pg.display.update()  # needed to blit the bg everywhere
        
    def _render(self):
        dirty_rects = self.sprites.draw(pview.screen, self.bg)
        pg.display.update(dirty_rects)
#         draw_hud(self.mana, self.mana_max)
        
        

def _make_bg():
    """ return surface """
    surf = pg.Surface(pview.size)
    surf.fill((11, 44, 44))
    surf.fill((33, 66, 66), T(0, 0, 800, 100))
    surf.convert()
    return surf


class Gauge(pg.sprite.DirtySprite):
    def __init__(self, v, vmax, rect0, color=(222, 22, 22), bgcolor=(0, 0, 0)):
        pg.sprite.DirtySprite.__init__(self)
        self.name = 'Mana'
        self.v = v
        self.vmax = vmax
        self.rect0 = rect0
        self.color = color
        self.bgcol = bgcolor
        self.refresh()
    
    def set(self, v, vmax):
        self.v = v
        self.vmax = vmax
        self.refresh()
                
    def refresh(self):
        b = 2  # border thickness
        x, y, w, h = self.rect0
        self.rect = pg.Rect((T(x) - b, T(y) - b, T(w) + 2 * b, T(h) + 2 * b))
        surf = pg.Surface((self.rect.w, self.rect.h))
        surf.fill(self.bgcol)  # empty part
        if self.v > 0:  # full part
            fh = h * self.v // self.vmax  # full part height  
            inner_rect = pg.Rect(b, T(h - fh) + b, T(w), T(fh))
            surf.fill(self.color, inner_rect)
        surf.convert()
        self.image = surf
        self.dirty = 1
        # TODO: draw 'Mana' below
#         ptext.draw('Mana', midtop=(T(x + w // 2), T(h + y) + b),
#                    fontsize=T(20), color=(222, 222, 222))

        
def draw_hud(v, vmax):
    """ draw top bar and gauges """
    
    b = 1  # border thickness
    # draw vertical gauge
    x, y, w, h = 100, 5, 20, 70
    vcol = 222, 111, 222
    bgcol = 55, 55, 55
    pview.fill(bgcol, (T(x) - b, T(y) - b, T(w) + 2 * b, T(h) + 2 * b))  # empty
    d = h * v // vmax
    pview.fill(vcol, (T(x), T(y + h - d), T(w), T(d)))  # gauge full
    ptext.draw('Mana', midtop=(T(x + w // 2), T(h + y) + b),
               fontsize=T(20), color=(222, 222, 222))
    # draw horizontal gauge
    d = 200 * v // vmax
    pview.fill((0, 0, 0), T(200 - 1, 5 - 1, 200 + 2, 15 + 2))  # gauge empty
    pview.fill((222, 111, 222), T(200, 5, d, 15))  # gauge full
    ptext.draw('Mana', midright=T(200 - 5, 5 + 15 // 2),
               fontsize=T(20), color=(222, 222, 222))
        

if __name__ == "__main__":
    from settings import FPS
    pg.init()
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    s = GameScene()
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True
                elif event.key == pg.K_F11:
                    pview.toggle_fullscreen()
                    s.refresh_view()
        ms = clock.tick(FPS)
        scene_id, kwargs = s.tick(ms)
        pg.display.set_caption('game scene %.1f' % clock.get_fps())
