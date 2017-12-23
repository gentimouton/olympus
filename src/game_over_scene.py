from controls import controller
import ptext
from pview import T
import pview
import pygame as pg
from scene import Scene, SCN_MENU


class GameOverScene(Scene):
    """ Main menu """
    
    def __init__(self):
        pass
    
    def tick(self, ms):
        if controller.btn_event('select'):
            return SCN_MENU, {}
        self._render()
        return None, {}
    
    def refresh_view(self):
        pass # no need to do anything until using dirty sprites
    
    def _render(self):
        pview.fill((22,22,22))
        pview.fill('red', T(100, 300, 450, 70))
        ptext.draw('Game over', T(150, 320), fontsize=T(70), color='black')
        pg.display.flip()
        

