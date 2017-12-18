""" The game scene has a HUD with gauges and a series of encounters. 
Player makes decisions during encounters, affecting gauges. 
Game is over when certain gauges reach certain states.
"""
from controls import controller
from encounter import Encounter
from game_bg import make_bg
from hud import Hud
import pview
import pygame as pg
from scene import SCN_MENU, Scene


class GameScene(Scene):        
    def __init__(self):
        # model
        self.state = {'mana': {'v': 10, 'vmax': 100} }  # can save this via pickle 
        # gfx
        self.bg = make_bg()
        self.sprites = pg.sprite.LayeredDirty()
        self.encounters = [Encounter(self.sprites)]  # TODO: add those to state
        self.hud = Hud(self.sprites, self.state)

        
    def tick(self, ms):
        if controller.btn_event('select'):
            return SCN_MENU, {}
        self._render()
        return None, {}
    
    def reset_resume(self):
        self.refresh_view()
        
    def refresh_view(self):
        self.bg = make_bg()
        pview.screen.blit(self.bg, (0, 0))
        for spr in self.sprites:
            spr.refresh()
        pg.display.update()  # needed to blit the bg everywhere
        
    def _render(self):
        dirty_rects = self.sprites.draw(pview.screen, self.bg)
        pg.display.update(dirty_rects)
        



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
