""" An encounter is a situation (text, image) and choices with consequences. """
from game_model import encounter_data
import pygame as pg
from utils import random_color, NeatSprite


class EncounterGfx():
    def __init__(self, enc_kind, spr_grp):  # TODO: should not know about spr_grp? 
        """ spr_grp is the current scene's sprite group """
        self.data = encounter_data[enc_kind]
        txt = self.data['txt']
        self.mid_card = Card((300, 150, 200, 300), random_color(), txt)
        txt = self.data['left']['txt']
        self.left_card = Card((50, 150, 200, 300), random_color(), txt)
        txt = self.data['right']['txt']
        self.right_card = Card((550, 150, 200, 300), random_color(), txt)
        spr_grp.add(self.mid_card, self.left_card, self.right_card)
        
    def kill(self):
        """ kill sprites. Could do a fancier animation, then kill them. """
        self.left_card.kill()
        self.mid_card.kill()
        self.right_card.kill()
        


class Card(NeatSprite): 
    def __init__(self, rect, color, txt):
        """ rect is a 4-tuple or a pygame Rect, 
        color is a 3-tuple or a pygame Color, 
        txt a string """
        NeatSprite.__init__(self, rect, color=color,
                           txt=txt, fontsize=24, txt_positioning='center',
                           bcol=(111, 111, 55), bthick=2)


if __name__ == "__main__":
    from settings import FPS
    import pview
    import random
    from game_model import ENC_DFLT
    from pview import T
    random.seed(2)
    pg.init()
    res = 800, 600
    pview.set_mode(res)
    clock = pg.time.Clock()
    # dummy data
    sprites = pg.sprite.LayeredDirty()
    gfx = EncounterGfx(ENC_DFLT, sprites)
    bgcol1 = random_color()
    bgcol2 = random_color()
    # make bg
    def make_dummy_bg():
        bg = pg.Surface(pview.size)
        bg.fill(bgcol1)
        for i in range(res[0] // 20 + 1):
            start = i * 20, 0
            end = i * 20, res[1]
            pg.draw.line(bg, bgcol2, T(start), T(end), T((i + 1) // 2))
        return bg
    bg = make_dummy_bg()
    # loop
    done = False
    while not done:
        # process inputs
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True
                elif event.key == pg.K_F11:
                    pview.toggle_fullscreen()
                    bg = make_dummy_bg()  # make bg fit new screen size
                    pview.screen.blit(bg, (0, 0))
                    pg.display.update()  # needed to blit the bg everywhere
                    for spr in sprites:
                        spr.recompute = 1
        for spr in sprites:
            spr.update() # process animations, redraw if changed resolution
        dirty_rects = sprites.draw(pview.screen, bg)
        pg.display.update(dirty_rects)
        clock.tick(FPS)
        pg.display.set_caption('game scene %.1f' % clock.get_fps())
