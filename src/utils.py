from random import randint as r

import ptext
from pview import T
import pygame as pg
import pview

def random_color():
    return r(22, 222), r(22, 222), r(22, 222)


_TRANSPARENT = 255, 0, 255  # magenta
class ResSprite(pg.sprite.DirtySprite):
    """ Responsive Sprite: automatically scales to screen resolution, 
    provided its `update` method is called.
    """
    def __init__(self, rect0, color=_TRANSPARENT, layer=1,
                 txt=None, fontsize=12,
                 txt_positioning='topleft',
                 txt_aa=True, txt_owidth=None, txt_ocolor=None,
                 bcol=None, bthick=0):
        """
        rect0: dimensions in the base resolution. Pygame rect or a 4-tuple. 
        color: optional, pygame color, string, or 3-tuple. Default transparent.
        layer: int in LayeredDirty group. Higher = foreground.
        txt: string, optional.
        fontsize: in px, default 12.
        txt_positioning: 'center', or 'topleft'. Default 'topleft'.
        txt_aa: boolean to antialias text.
        txt_owidth: outline thickness
        txt_ocolor: outline color, 1 is a good value - means 1/24 of font size.
        bcol: border color, 
        bthick: border thickness, in pixels, fixed across resolutions.
        Works like an inner padding, does not overflow the assigned rect.
        """
        pg.sprite.DirtySprite.__init__(self)
        self.rect0 = pg.Rect(rect0)  # Rect(Rect(x,y,w,h)) == Rect(x,y,w,h)
        # TODO: too many props. Use a dict for text and positioning instead?
        self.layer = layer
        self.color = color
        self.bcol = bcol
        self.bthick = bthick
        self._txt = txt
        self.fontsize = fontsize
        self.txt_positioning = txt_positioning
        self.txt_aa = txt_aa
        self.txt_owidth = txt_owidth
        self.txt_ocolor = txt_ocolor
        self.recompute = 1 # similar to DirtySprite.dirty

    def _recompute(self):
        """ recompute image and rect after screen resolution changed,
        or after txt changed. """
        self._res = pview.size  # resolution this spr is for
        self.rect = T(self.rect0)
        w, h = self.rect.size
        surf = pg.Surface((w, h))
        b = self.bthick
        inner_rect = pg.Rect(b, b, w - 2 * b, h - 2 * b)
        if self.bcol:
            surf.fill(self.bcol)  # draw border
        surf.fill(self.color, inner_rect)  # draw inner part
        if self._txt:
            txt_kwargs = {
                'width': inner_rect.w,
                'fontsize': T(self.fontsize),
                'antialias': self.txt_aa,
                'owidth': self.txt_owidth,
                'ocolor': self.txt_ocolor,
                'surf': surf
                }
            if self.txt_positioning == 'center':
                txt_kwargs['center'] = w // 2, h // 2
            elif self.txt_positioning == 'topleft':
                txt_kwargs['pos'] = 0, 0 
            ptext.draw(self._txt, **txt_kwargs)
        surf.set_colorkey(_TRANSPARENT, pg.RLEACCEL)
        surf.convert()
        self.image = surf
        self.dirty = 1
        self.recompute = 0

    def set_txt(self, txt):
        if txt != self._txt:
            self._txt = txt
            self._recompute()
        
    def update(self, *args, **kwargs):
        if self.recompute or pview.size != self._res:
            self._recompute()

