from controls import controller
import ptext
from pview import T
import pview
import pygame as pg
from scene import Scene, SCN_GAME, SCN_QUIT


class MenuScene(Scene):
    """ Main menu """
    
    def __init__(self):
        self._menu_choice = 0
        self._callbacks = [ (SCN_GAME, {}), (SCN_QUIT, {})]
        
    def tick(self, ms):
        if controller.btn_event('select'):
            return self._callbacks[self._menu_choice]    
        elif controller.btn_event('down'):
            self._menu_choice = (self._menu_choice + 1) % len(self._callbacks) 
        elif controller.btn_event('up'):
            self._menu_choice = (self._menu_choice - 1) % len(self._callbacks)

        self._render()
        return None, {}  # ugly, wish i could do without it
    
    
    def _render(self):
        pview.fill((0, 111, 111))
        
        ptext.draw('Play', T(300, 200), fontsize=T(70), color='black')
        ptext.draw('Quit', T(300, 300), fontsize=T(70), color='black')
        ptext.draw('>', T(250, 200 + self._menu_choice * 100),
                   fontsize=T(70), color='black')
        
        ptext.draw('F11: toggle fullscreen\nEsc: quit', T(10, 10),
            fontsize=T(20), color='black')
        
#         pg.draw.rect(pview.screen, (0, 0, 111), T(100, 100, 200, 200))
    


if __name__ == "__main__":
    pg.init()
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    s = MenuScene()
    while not any(event.type in (pg.KEYDOWN, pg.QUIT) for event in pg.event.get()):
        ms = clock.tick(30)        
        scene_id, kwargs = s.tick(ms)
        ptext.draw('demo - press any key to exit', topright=T(790, 10),
                   fontsize=T(30), color='red', background='white')
        pg.display.flip()  # render