""" heads up display. Bunch of gauges and icons and text. """
import pview
import pygame as pg
from utils import NeatSprite, TRANSPARENT, Shape
from pview import T

class Hud(): # TODO: HUD and EncounterRenderer should inherit from Renderer
    def __init__(self, state, rect0):
        """ Render parts of the game state.
        state: entire model from game scene. Use it read-only.
        rect0: area of the screen (in base resolution) to render hud. 
        """
        self._res = pview.size  # memorize current resolution
        self.state = state
        self.rect0 = pg.Rect(rect0)  # pg.Rect(pg.Rect(tuple)) == pg.Rect(tuple)
        # build widgets
        gauge = Gauge(lambda: self.state.mana,  # tell widget how to fetch data
                      lambda: self.state.mana_max,
                      (100, 5, 20, 70))
        icon = ManaIcon((100 + 2, 80, 16, 16))
        self.sprites = pg.sprite.LayeredDirty([gauge, icon])      
        self.stale = 1  # also set to 1 by GameScene if game state changed
        
        
    def draw(self):
        """ Update/redraw all the gauges and icons and texts. """
        self.bg = pg.Surface(T(self.rect0.size))
        self.bg.fill((111, 111, 222))
        pview.screen.blit(self.bg, T(self.rect0.topleft))
        pg.display.update(T(self.rect0))
        for spr in self.sprites:
            spr.recompute = 1
        self._res = pview.size
        self.stale = 0


    def tick(self, ms):
        if self._res != pview.size or self.stale:  # resolution or state changed
            self.draw()  # (re)create sprites, set them to recompute
        self.sprites.update()  # (re)compute sprites, set them to dirty
        dirty_rects = self.sprites.draw(pview.screen)  # blit dirty sprites
        pg.display.update(dirty_rects)  # flip dirty sprites' areas



class ManaIcon(NeatSprite):
    """ Static icon. Square with a hole in the middle. """
    def __init__(self, rect0):
        w, h = rect0[2], rect0[3]
        shape = Shape('rect', (w // 4, h // 4, w // 2, h // 2), TRANSPARENT)
        NeatSprite.__init__(self, rect0, color=(255, 0, 0), shapes=[shape])


class Gauge(NeatSprite):
    """ Rectangle filled with smaller rect inside. """
    def __init__(self, vfunc, vmaxfunc, rect0,
                 color=(222, 22, 22), bgcolor=(0, 0, 0)):
        NeatSprite.__init__(self, rect0, bgcolor, bthick=2)
        self._gauge_color = color
        self.vfunc = vfunc  # function to fetch latest value from game state
        self.vmaxfunc = vmaxfunc
        self.v = None  # set in self.update()
        self.vmax = None
        
    def update(self, *args, **kwargs):
        """ Update gauge's value if it changed in the game state. """
        v = self.vfunc()
        vmax = self.vmaxfunc()
        if self.v != v or self.vmax != vmax:  # values changed in game state
            self.v = v
            self.vmax = vmax
            w, h = self.rect0.size  # rect0 from parent class
            fh = h * v // self.vmax  # height of full part, in base resolution
            shape = Shape('rect', (0, h - fh, w, fh), self._gauge_color)
            self.set_shapes([shape])
        NeatSprite.update(self)
        


if __name__ == "__main__":
    import settings
    pg.init()
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    # dummy data
    class DummyState():
        def __init__(self):
            self.mana = 20
            self.mana_max = 100
    state = DummyState()
    hud = Hud(state, (0, 0, 800, 100))
    # loop
    done = False
    while not done:
        for event in pg.event.get():  # process inputs
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True
                elif event.key == pg.K_F11:
                    pview.toggle_fullscreen()
                    hud.stale = 1
        ms = clock.tick(settings.FPS)
        hud.tick(ms)
        
        pg.display.set_caption('game scene %.1f' % clock.get_fps())
