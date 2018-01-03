""" The game scene has a HUD with gauges and a series of encounters. 
Player makes decisions during encounters, affecting game state. 
If game state is lost, call game over scene.
Can also pause game and go to main menu, passing an option to resume game.
"""

import random

from constants import CMD_NEWG, CMD_RESM
from controls import controller
from encounter_gfx import EncounterRenderer
from game_model import GameModel, GST_LOST
import pview
import pygame as pg
from scene import SCN_MENU, Scene, SCN_OVER
import settings
from utils import NeatSprite


random.seed(1)


class GameScene(Scene):
    def __init__(self):
        # load images and sounds from disk here
        self._build_new_game()
        
    def _build_new_game(self):
        self.model = GameModel()
        self.sprites = pg.sprite.LayeredDirty()
        self.enc = EncounterRenderer(self.model, (0, 100, 800, 500))
        # TODO: add back the HUD
#         if settings.DEBUG: # TODO: add back debug spr
#             self._debug_spr = DebugSpr(self)
#             self.sprites.add(self._debug_spr)
        
    def tick(self, ms):
        # process player inputs
        if controller.btn_event('select'):
            return SCN_MENU, {'can_resume':1}  # add "Resume Game" to menu scene
        if controller.btn_event('left'):
            self.model.choose('left')
            self.enc.stale = 1 # model changed: tell renderer to redraw
        if controller.btn_event('right'):
            self.model.choose('right')
            self.enc.stale = 1
        if self.model.game_status == GST_LOST:
            return SCN_OVER, {'enc_seen': self.model.encounters_seen}
        # tick renderers
        self.enc.tick(ms)
        return None, {}


    def resume(self, **kwargs):
        """ Scene callback. Called from the menu scene via scene manager. """
        if kwargs['cmd'] == CMD_NEWG:
            self._build_new_game()
        elif kwargs['cmd'] == CMD_RESM:
            pass
        self.enc.stale = 1
        
        

class DebugSpr(NeatSprite):
    """ Hack class to display state of the game scene on screen """
    def __init__(self, gs):
        NeatSprite.__init__(self, (600, 550, 200, 50), layer=100, fontsize=16,
                           txt_aa=False, txt_owidth=2, txt_ocolor=(0, 0, 0))
        self.gs = gs
        
    def update(self):
        state = self.gs.model
        txt = '--debug--\n%d encounters under\nmana %d\nseen %d encounters' % (
            len(state.encounters), state.mana, state.encounters_seen
            )
        self.set_txt(txt)
        NeatSprite.update(self)  # redraw if needed
        
        
if __name__ == "__main__":
    pg.init()
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    scene = GameScene()
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
        ms = clock.tick(settings.FPS)
        scene_id, kwargs = scene.tick(ms)
        pg.display.set_caption('game scene %.1f' % clock.get_fps())
