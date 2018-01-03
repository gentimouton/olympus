from controls import controller
import ptext
from pview import T
import pview
import pygame as pg
from scene import Scene, SCN_MENU


class GameOverScene(Scene):
    
    def __init__(self):
        self.enc_seen = None
    
    def tick(self, ms):
        if controller.btn_event('select'):
            return SCN_MENU, {}
        self._draw()
        return None, {}
    
    def resume(self, **kwargs):
        """ called by scene manager when the game scene ends. 
        kwargs passed by game scene. 
        """
        self.enc_seen = kwargs['enc_seen']
        # TODO: say why the game ended, via constants file probably
        
    def _draw(self):
        pview.fill((0, 0, 0))
        txt = 'Game over\n%d encounters seen' % self.enc_seen
        ptext.draw(txt, T(150, 320), fontsize=T(70),
                   color='black', background='red')
        pg.display.flip()
