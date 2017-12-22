""" The game scene has a HUD with gauges and a series of encounters. 
Player makes decisions during encounters, affecting gauges. 
Game is over when certain gauges reach certain states.
"""

import random

from controls import controller
from encounter_gfx import EncounterGfx
from game_bg import make_bg
from game_model import GameModel
from hud import Hud
import pview
import pygame as pg
from scene import SCN_MENU, Scene
import settings
from utils import NeatSprite


random.seed(1)


class GameScene(Scene):
    def __init__(self):
        self.model = GameModel()
        # gfx
        self.bg = make_bg()
        self.sprites = pg.sprite.LayeredDirty()
        self.encounter_gfx = None
        self._display_encounter()
        self.hud = Hud(self.sprites, self.model)
        if settings.DEBUG:
            self._debug_spr = DebugSpr(self)
            self.sprites.add(self._debug_spr)

    def _display_encounter(self):
        try:
            self.encounter_gfx.kill()  # remove enc sprites from sprite group
        except AttributeError:  # self.encounter is None
            pass
        self.encounter_gfx = EncounterGfx(self.model.cur_enc, self.sprites)
        
    def tick(self, ms):
        # process player inputs
        if controller.btn_event('select'):
            return SCN_MENU, {}
        if controller.btn_event('left'):
            self.model.choose('left')
            self.hud.update()
            self._display_encounter()
        if controller.btn_event('right'):
            self.model.choose('right')
            self.hud.update()
            self._display_encounter()
        # update graphics
        self._render()
        return None, {}

    def reset_resume(self):
        self.refresh_view()
        
    def refresh_view(self):
        self.bg = make_bg()
        pview.screen.blit(self.bg, (0, 0))
        for spr in self.sprites:
            spr.recompute = 1
        pg.display.update()  # needed to blit the bg everywhere
        
    def _render(self):
        """ draw dirty sprites, if any. Typically nothing to do. """
        self.sprites.update()
        dirty_rects = self.sprites.draw(pview.screen, self.bg)
        pg.display.update(dirty_rects)
        

class DebugSpr(NeatSprite):
    """ Hack class to display state of the game scene on screen """
    def __init__(self, gs):
        NeatSprite.__init__(self, (600, 550, 200, 50), layer=100, fontsize=16,
                           txt_aa=False, txt_owidth=2, txt_ocolor=(0, 0, 0))
        self.gs = gs
        
    def update(self):
        txt = '--debug--\n%d encounters under' % len(self.gs.model.encounters)
        self.set_txt(txt)
        NeatSprite.update(self)  # redraw if needed
        
        
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
