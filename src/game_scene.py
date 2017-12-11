import pygame as pg
from controls import controller
from scene import SCN_MENU, Scene
import pview
from pview import T


class GameScene(Scene):
    
    def tick(self, ms):
        if controller.btn_event('select'):
            return SCN_MENU, {}
        
        self._render()
        return None, {}
    
    def _render(self):
        pview.fill((100, 0, 100))
        pg.draw.rect(pview.screen, (222, 0, 111), T(500, 300, 200, 50))