from game_model import encounter_data
import pygame as pg
from utils import NeatSprite
from pview import T
import pview

class EncounterRenderer():
    def __init__(self, state, rect0): 
        """ Render encounters.
        state: entire model from game scene.
        rect0: area of the screen (in base resolution) to render encounters. 
        """
        self._res = pview.size  # memorize current resolution
        self.state = state
        self.rect0 = pg.Rect(rect0)  # pg.Rect(pg.Rect(tuple)) == pg.Rect(tuple)
        self.stale = 1  # also set to 1 by GameScene if game state changed
        
    
    def draw(self):
        """ Draw all elements of encounter: bg, problem, and 2 choices. """
        data = encounter_data[self.state.cur_enc]
        self.bg = pg.Surface(T(self.rect0.size))
        self.bg.fill(data['bgcolor'])
        x0, y0 = self.rect0.topleft
        pview.screen.blit(self.bg, T(x0, y0))
        pg.display.update(T(self.rect0))
        self.mid_card = Card((x0 + 300, y0 + 50, 200, 300),
                             data['mid']['bgcolor'],
                             data['mid']['txt'])
        self.left_card = Card((x0 + 50, y0 + 50, 200, 300),
                              data['left']['bgcolor'],
                              data['left']['txt'])
        self.right_card = Card((x0 + 550, y0 + 50, 200, 300),
                               data['right']['bgcolor'],
                               data['right']['txt'])
        self.sprites = pg.sprite.LayeredDirty()
        self.sprites.add(self.mid_card, self.left_card, self.right_card)
        self._res = pview.size
        self.stale = 0
        
    
    def tick(self, ms):
        if self._res != pview.size or self.stale:  # resolution or state changed
            self.draw()  # (re)create sprites, set them to recompute
        self.sprites.update()  # (re)compute sprites, set them to dirty
        dirty_rects = self.sprites.draw(pview.screen)  # blit dirty sprites
        pg.display.update(dirty_rects)  # flip dirty sprites' areas

            


class Card(NeatSprite): 
    def __init__(self, rect0, color, txt):
        """ Representation of the encounter's problem and choices. 
        rect0: area of sprite in the screen. 4-tuple or pygame Rect in base res. 
        color: 3-tuple or pygame Color.
        txt: string 
        """
        NeatSprite.__init__(self, rect0, color=color,
                           txt=txt, fontsize=24, txt_positioning='center',
                           bcol=(111, 111, 55), bthick=2)



if __name__ == "__main__":
    import settings
    import random
    from game_model import ENC_DFLT
    random.seed(2)
    pg.init()
    res = 800, 600
    pview.set_mode(res)
    clock = pg.time.Clock()
    # dummy data
    class DummyState():
        def __init__(self):
            self.cur_enc = ENC_DFLT
    state = DummyState()
    enc = EncounterRenderer(state, (0, 100, 800, 500))
    # loop
    done = False
    while not done:
        for event in pg.event.get(): # process inputs
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True
                elif event.key == pg.K_F11:
                    pview.toggle_fullscreen()
                    enc.stale = 1
        ms = clock.tick(settings.FPS)
        enc.tick(ms)
        
        pg.display.set_caption('game scene %.1f' % clock.get_fps())
