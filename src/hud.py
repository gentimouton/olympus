""" heads up display. bunch of gauges and icons and text. """
from utils import ResSprite


# TODO: take care of hud bg in here, not in game_bg

class Hud():
    def __init__(self, spr_grp, state):
        # TODO: pass a rect saying where the HUD lives
        self.state = state
        v, vmax = state.mana, state.mana_max
        self.gauge = Gauge(v, vmax, (100, 5, 20, 70))
        self.icon = ManaIcon((100 + 2, 80, 16, 16))
        spr_grp.add(self.gauge, self.icon)
        
    def update(self):
        v, vmax = self.state.mana, self.state.mana_max
        self.gauge.set(v, vmax)


class ManaIcon(ResSprite):
    """ static icon. Square with a hole in the middle. """
    def __init__(self, rect):
        ResSprite.__init__(self, rect, color=(255, 0, 0))
        # make square hole
#         hole = T(w // 4), T(h // 4), T(w // 2), T(h // 2) 
#         surf.fill((255, 0, 255), hole)
#         surf.set_colorkey((255, 0, 255), pg.RLEACCEL)
        # TODO: make hole: break down _recompute into subparts, one accepting a surf, one returning T(rect)?


class Gauge(ResSprite):
    def __init__(self, v, vmax, rect, color=(222, 22, 22), bgcolor=(0, 0, 0)):
        ResSprite.__init__(self, rect, color, bcol=bgcolor, bthick=2)
        self.v = v
        self.vmax = vmax
        
    def set(self, v, vmax):
        self.v = v
        self.vmax = vmax
        self.recompute = 1
    
# TODO: draw gauge properly, by breaking down _recompute 
#         if self.v > 0:  # full part
#             fh = (h - b * 2) * self.v // self.vmax  # height of full part   
#             inner_rect = pg.Rect(b, h - fh - b, w - b * 2, fh)
#             surf.fill(self.color, inner_rect)
