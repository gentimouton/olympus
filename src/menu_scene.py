from controls import controller
import ptext
from pview import T
import pview
import pygame as pg
from scene import Scene, SCN_GAME, SCN_QUIT
from constants import CMD_NEWG, CMD_RESM

class MenuScene(Scene):
    """ Main menu """
    
    def __init__(self):
        self._menu_choice = 0
        self._callbacks = [ 
            (SCN_GAME, {'cmd': CMD_NEWG}),
            (SCN_GAME, {'cmd': CMD_RESM}),
            (SCN_QUIT, {})
            ]
        
    def tick(self, ms):
        if controller.btn_event('select'):
            return self._callbacks[self._menu_choice]
        elif controller.btn_event('down'):
            self._menu_choice = (self._menu_choice + 1) % len(self._callbacks) 
        elif controller.btn_event('up'):
            self._menu_choice = (self._menu_choice - 1) % len(self._callbacks)
        self._render()
        return None, {}
    
    def refresh_view(self):
        pass  # no need to do anything until using dirty sprites
    
    def _render(self):
        pview.fill('black')
        ptext.draw('New Game', T(200, 200), fontsize=T(70))
        ptext.draw('Resume', T(200, 300), fontsize=T(70))
        ptext.draw('Quit', T(200, 400), fontsize=T(70))
        ptext.draw('>', T(150, 200 + self._menu_choice * 100), fontsize=T(70))
        ptext.draw('F11: toggle fullscreen\nEsc: quit', T(10, 10), fontsize=T(20))
        pg.display.flip()
        

if __name__ == "__main__":
    from settings import FPS
    pg.init()
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    s = MenuScene()
    while not pg.event.peek([pg.QUIT, pg.KEYDOWN]):
        ms = clock.tick(FPS)        
        scene_id, kwargs = s.tick(ms)
        
