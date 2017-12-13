from controls import controller
import ptext
from pview import T
import pview
import pygame as pg
from scene import SCN_MENU, Scene


class GameScene(Scene):
    """ Centerpiece of the game """
        
    def __init__(self):
        self.mana = 10
        self.mana_max = 100
        
    def tick(self, ms):
        if controller.btn_event('select'):
            return SCN_MENU, {}
        
        self._render()
        return None, {}
    
    def refresh_view(self):
        pass  # no need to do anything until using dirty sprites
    
    def _render(self):
        pview.fill((22, 55, 55))
        # draw top bar and gauges
        pview.fill((33, 66, 66), T(0, 0, 800, 100))
        pview.fill((0, 0, 0), T(100 - 1, 5 - 1, 20 + 2, 70 + 2))  # gauge empty
        d = 70 * self.mana // self.mana_max
        pview.fill((222, 111, 222), T(100, 5 + 70 - d, 20, d))  # gauge full
        ptext.draw('Mana', midtop=T(100 + 20 // 2, 70 + 5 + 2),
                   fontsize=T(20), color=(222, 222, 222))
        # draw horizontal gauge instead?
        d = 200 * self.mana // self.mana_max
        pview.fill((0, 0, 0), T(200 - 1, 5 - 1, 200 + 2, 15 + 2))  # gauge empty
        pview.fill((222, 111, 222), T(200, 5, d, 15))  # gauge full
        ptext.draw('Mana', midright=T(200 - 5, 5 + 15 // 2),
                   fontsize=T(20), color=(222, 222, 222))
        # card contours
        pview.fill((111, 111, 55), T(50 - 1, 150 - 1, 200 + 2, 300 + 2))
        pview.fill((111, 111, 55), T(300 - 1, 150 - 1, 200 + 2, 300 + 2))
        pview.fill((111, 111, 55), T(550 - 1, 150 - 1, 200 + 2, 300 + 2))
        # cards
        pview.fill((55, 55, 111), T(50, 150, 200, 300))
        pview.fill((55, 55, 55), T(300, 150, 200, 300))
        pview.fill((111, 55, 55), T(550, 150, 200, 300))
        
        

class Card():
    def __init__(self, txt, opt1, opt2):
        self.txt = txt
        self.opt1 = opt1
        self.opt2 = opt2
        

if __name__ == "__main__":
    pg.init()
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    s = GameScene()
    while not any(event.type in (pg.KEYDOWN, pg.QUIT) for event in pg.event.get()):
        ms = clock.tick(30)        
        scene_id, kwargs = s.tick(ms)
        ptext.draw('test screen - press any key to exit', topright=T(790, 10),
                   fontsize=T(30), color='red', background='white')
        pg.display.flip()  # render
