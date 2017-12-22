""" heads up display. bunch of gauges and icons and text. """
from utils import NeatSprite, TRANSPARENT, Shape


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


class ManaIcon(NeatSprite):
    """ static icon. Square with a hole in the middle. """
    def __init__(self, rect):
        w, h = rect[2], rect[3]
        shape = Shape('rect', (w // 4, h // 4, w // 2, h // 2), TRANSPARENT)
        NeatSprite.__init__(self, rect, color=(255, 0, 0), shapes=[shape])


class Gauge(NeatSprite):
    def __init__(self, v, vmax, rect, color=(222, 22, 22), bgcolor=(0, 0, 0)):
        NeatSprite.__init__(self, rect, bgcolor, bthick=2)
        self._gauge_color = color
        self.set(v, vmax)
        
    def set(self, v, vmax):
        self.v = v
        self.vmax = vmax
        w, h = self.rect0.size # rect0 from parent class
        if self.v > 0:  # draw full part of gauge
            fh = (h * self.v) // self.vmax  # height of full part, in base resolution
            shape = Shape('rect', (0, 0, w, fh), self._gauge_color)
            self.set_shapes([shape])
        
