""" The game scene has a HUD with gauges and a series of encounters. 
Player makes decisions during encounters, affecting game state. 
If game state is lost, call game over scene.
Can also pause game and go to main menu, passing an option to resume game.
"""

import random

from constants import CMD_NEWG, CMD_RESM
from controls import controller
from encounter_render import EncounterRenderer
from game_model import GameModel, GST_LOST
from hud import Hud
import pygame as pg
from scene import SCN_MENU, Scene, SCN_OVER
import settings


random.seed(1)


class GameScene(Scene):
    def __init__(self):
        # load images and sounds from disk here
        self._build_new_game()
        
    def tick(self, ms):
        # process player inputs
        if controller.btn_event('select'):
            return SCN_MENU, {'can_resume':1}  # add "Resume Game" to menu scene
        if controller.btn_event('left'):
            self.model.choose('left')
            self._set_renderers_stale()
        if controller.btn_event('right'):
            self.model.choose('right')
            self._set_renderers_stale()
        if self.model.game_status == GST_LOST:
            return SCN_OVER, {'enc_seen': self.model.encounters_seen}
        # tick renderers
        self.enc.tick(ms)
        self.hud.tick(ms)
        return None, {}

    def resume(self, **kwargs):
        """ Scene callback. Called from the menu scene via scene manager. """
        if kwargs['cmd'] == CMD_NEWG:
            self._build_new_game()
        elif kwargs['cmd'] == CMD_RESM:
            pass
        self._set_renderers_stale()

    def _build_new_game(self):
        self.model = GameModel()
        self.sprites = pg.sprite.LayeredDirty()
        self.enc = EncounterRenderer(self.model, (0, 100, 800, 500))
        self.hud = Hud(self.model, (0, 0, 800, 100))

    def _set_renderers_stale(self): # model changed: tell renderers to redraw
        self.enc.stale = 1  
        self.hud.stale = 1
        
        
if __name__ == "__main__":
    import pview
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
