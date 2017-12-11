import pygame as pg
from controls import controller
from scene import SCN_1, Scene


class Scene2(Scene):
    
    def tick(self, ms):
        if controller.btn_isdown('select'):
            return SCN_1, {}
        
        self._render()
        return None, {}
    
    def _render(self):
        screen = pg.display.get_surface()
        screen.fill((0, 100, 100))
