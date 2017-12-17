from controls import controller
import ptext
from pview import T
import pview
import pygame as pg
from scene import SCN_MENU, Scene


class GameScene(Scene):
    """ Centerpiece of the game """
        
    def __init__(self):
        # model
        self.mana = 10
        self.mana_max = 100
        # gfx
        self.card_sprites = pg.sprite.Group()
        self.encounters = [Encounter(self.card_sprites)]
        
    def tick(self, ms):
        if controller.btn_event('select'):
            return SCN_MENU, {}
        self._render()
        return None, {}
    
    def refresh_view(self):
        for spr in self.card_sprites:
            spr.refresh()
    
    def _render(self):
        pview.fill((22, 55, 55))  # bg
        draw_hud(self.mana, self.mana_max)
        self.card_sprites.draw(pview.screen)
        
def draw_hud(v, vmax):
    """ draw top bar and gauges """
    pview.fill((33, 66, 66), T(0, 0, 800, 100))
    b = 1  # border thickness
    # draw vertical gauge
    x, y, w, h = 100, 5, 20, 70
    vcol = 222, 111, 222
    bgcol = 55, 55, 55
    pview.fill(bgcol, (T(x) - b, T(y) - b, T(w) + 2 * b, T(h) + 2 * b))  # empty
    d = h * v // vmax
    pview.fill(vcol, (T(x), T(y + h - d), T(w), T(d)))  # gauge full
    ptext.draw('Mana', midtop=(T(x + w // 2), T(h + y) + b),
               fontsize=T(20), color=(222, 222, 222))
    # draw horizontal gauge
    d = 200 * v // vmax
    pview.fill((0, 0, 0), T(200 - 1, 5 - 1, 200 + 2, 15 + 2))  # gauge empty
    pview.fill((222, 111, 222), T(200, 5, d, 15))  # gauge full
    ptext.draw('Mana', midright=T(200 - 5, 5 + 15 // 2),
               fontsize=T(20), color=(222, 222, 222))
        

class Encounter():
    def __init__(self, spr_grp):
        self.txt = 'what do you do?'
        self.opt1 = 'a'
        self.opt2 = 'b'
        self.mid_card = Card((300, 150, 200, 300), (55, 55, 55), self.txt)
        self.left_card = Card((50, 150, 200, 300), (55, 55, 111), self.opt1)
        self.right_card = Card((550, 150, 200, 300), (111, 55, 55), self.opt2)
        spr_grp.add(self.mid_card, self.left_card, self.right_card)
        
        
        
class Card(pg.sprite.Sprite):
    def __init__(self, rect, color, txt):
        pg.sprite.Sprite.__init__(self)
        self.rect0 = rect
        self.color = color
        self.txt = txt
        self.refresh()
    
    def refresh(self):
        x, y, w, h = self.rect0
        inner_rect = (1, 1, T(w), T(h))
        self.rect = T(x) - 1, T(y) - 1, T(w) + 2, T(h) + 2
        surf = pg.Surface((T(w) + 2, T(h) + 2))
        surf.fill((111, 111, 55))
        surf.fill(self.color, inner_rect)
        surf.convert()
        self.image = surf
        

if __name__ == "__main__":
    pg.init()
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    s = GameScene()
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
                    s.refresh_view()
        ms = clock.tick(30)
        scene_id, kwargs = s.tick(ms)
        ptext.draw('ESC: exit\nF11: full', topright=T(790, 10),
                   fontsize=T(30), color='red', background='white')
        pg.display.flip()  # render
        
