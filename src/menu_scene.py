from controls import controller
import ptext
from pview import T
import pview
import pygame as pg
from scene import Scene, SCN_GAME, SCN_QUIT
from constants import CMD_NEWG, CMD_RESM

class MenuScene(Scene):
    """ Main menu.
    Display New Game and Quit.
    When a game has been started and is not over, enable Resume.
    """
    
    def __init__(self):
        self._choice = 0
        self._choices = [ 
            ('New game', SCN_GAME, {'cmd': CMD_NEWG}),
            ('Quit', SCN_QUIT, {})
            ]
        
    def tick(self, ms):
        if controller.btn_event('select'):
            c = self._choices[self._choice]
            return c[1], c[2] 
        elif controller.btn_event('down'):
            self._choice = (self._choice + 1) % len(self._choices)
        elif controller.btn_event('up'):
            self._choice = (self._choice - 1) % len(self._choices)
        self._draw()
        return None, {}

    def resume(self, **kwargs):
        """ called by scene manager from the game scene, passing kwargs. """
        self._choice = 0
        if kwargs.get('can_resume'):
            self._choices = [
                ('Resume', SCN_GAME, {'cmd': CMD_RESM}), 
                ('New game', SCN_GAME, {'cmd': CMD_NEWG}),
                ('Quit', SCN_QUIT, {})
                ]            
        else:
            self._choices = [ 
                ('New game', SCN_GAME, {'cmd': CMD_NEWG}),
                ('Quit', SCN_QUIT, {})
                ]
            
#     def redraw(self):
#         pass  # no need to do anything until using dirty sprites
    
    def _draw(self):
        pview.fill('black')
        for i, choice in enumerate(self._choices):
            ptext.draw(choice[0], T(200, 200 + i * 100), fontsize=T(70))
        ptext.draw('>', T(150, 200 + self._choice * 100), fontsize=T(70))
        ptext.draw('F11: toggle fullscreen\nEsc: quit', T(10, 10), fontsize=T(20))
        pg.display.flip()
        

if __name__ == "__main__":
    from settings import FPS
    pg.init()
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    scene = MenuScene()
    while not pg.event.peek([pg.QUIT, pg.KEYDOWN]):
        ms = clock.tick(FPS)        
        scene_id, kwargs = scene.tick(ms)
        
