from controls import controller
import pygame as pg
from scene import Scene, SCN_2


class Scene1(Scene):
    
    def __init__(self):
        pass 
        
    def tick(self, ms):
        if controller.btn_isdown('select'):
            return SCN_2, {'arg_key': 'arg_value'}
        self._render()
        return None, {}
    
    def _render(self):
        screen = pg.display.get_surface()
        screen.fill((100, 100, 0))
