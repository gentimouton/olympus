""" The game scene has a HUD with gauges and a series of encounters. 
Player makes decisions during encounters, affecting gauges. 
Game is over when certain gauges reach certain states.
"""
from collections import deque
from random import seed 

from controls import controller
from encounter import Encounter
from game_bg import make_bg
from hud import Hud
import pview
import pygame as pg
from scene import SCN_MENU, Scene, SCN_QUIT


seed(1)

class GameScene(Scene):        
    def __init__(self):
        # model
        self.state = {'mana': {'v': 10, 'vmax': 100},
                      'encounters': ['default', 'default']  # encounter ids
                       }  # can save this via pickle 
        # TODO: make this a class in module, with save()/load() module funcs.
        # gfx
        self.bg = make_bg()
        self.sprites = pg.sprite.LayeredDirty()
        self.encounters = deque([
            Encounter(self.sprites),
            Encounter(self.sprites)
            ])  # TODO: add encounters to state
        self.encounter = self.encounters.popleft()
        self.hud = Hud(self.sprites, self.state)

        
    def tick(self, ms):
        # process player inputs
        if controller.btn_event('select'):
            return SCN_MENU, {}
        if controller.btn_event('left'):
            self.encounter.choose_left(self.state)  # modify state by side effect
            try:
                self.encounter = self.encounters.popleft()
            except IndexError:  # empty
                print('game over')  # TODO: add cards instead.
                return SCN_QUIT, {}
            self.hud.update()
        if controller.btn_event('right'):
            self.encounter.choose_right(self.state)  # modify state by side effect
            try:
                self.encounter = self.encounters.popleft()
            except IndexError:  # empty
                print('game over')  # TODO: add cards instead.
                return SCN_QUIT, {}
            self.hud.update() # TODO: 1) dupe code, 2) may need to update state? 
        
        # update graphics
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
        """ draw dirty sprites, if any. Typically nothing to do. """
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
