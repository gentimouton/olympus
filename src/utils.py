from random import randint

import ptext
from pview import T
import pview
import pygame as pg


def random_color():
    return randint(22, 222), randint(22, 222), randint(22, 222)


TRANSPARENT = 255, 0, 255  # magenta

class Shape():
    """ container for NeatSprite to draw shapes like rect and circle.
    Used by subclasses of NeatSprite to pass the shapes to draw.
    Example: Shape('rect', (0,0,200,10), (0,222,0))
    Provide shape dimensions ignoring the border thickness of parent sprite.
    Example: if parent rect.w = 10 and border thickness = 1, passing a rect of 
    (2,y,10,h) will convert it internally to (1+T(2), y, T(10)-2, h)     
    """
    def __init__(self, kind, dims, color):
        self.kind = kind
        self.dims = dims
        self.color = color

class NeatSprite(pg.sprite.DirtySprite):
    """ Responsive Sprite: automatically scales to screen resolution, 
    provided its `update` method is called.
    """
    def __init__(self, rect0, color=TRANSPARENT, shapes=[], layer=1,
                 txt=None, fontsize=12,
                 txt_positioning='topleft',
                 txt_aa=True, txt_owidth=None, txt_ocolor=None,
                 bcol=None, bthick=0):
        """
        rect0: dimensions in the base resolution. Pygame rect or a 4-tuple. 
        color: optional, pygame color, string, or 3-tuple. Default transparent.
        shapes: ordered list of Shapes
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
        self.shapes = shapes
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
        self.recompute = 1  # similar to DirtySprite.dirty

    def _recompute(self):
        """ recompute image and rect after screen res, shapes, or text changed. 
        First fill bg color, then draw shapes in order, and finish with text.
        """
        self._res = pview.size  # resolution this spr is for
        self.rect = T(self.rect0)
        tw, th = self.rect.size
        surf = pg.Surface((tw, th))
        
        # draw border and fill with background color
        b = self.bthick
        inner_rect = pg.Rect(b, b, tw - 2 * b, th - 2 * b)  # inner part
        if self.bcol:
            surf.fill(self.bcol)  # draw border
        surf.fill(self.color, inner_rect)
        
        # draw shapes
        for shape in self.shapes:
            if shape.kind == 'rect':
                x, y, w, h = shape.dims
                xx = b + T(x)* inner_rect.w // self.rect.w # fit into inner rect
                yy = b + T(y) * inner_rect.h // self.rect.h 
                ww = T(w) * inner_rect.w // self.rect.w 
                hh = T(h) * inner_rect.h // self.rect.h
                shape_rect = pg.Rect(xx, yy, ww, hh)
                surf.fill(shape.color, shape_rect)
            else:
                txt = 'NeatSprite: unsupported Shape.kind: %s' % shape.kind
                raise NotImplementedError(txt)
                
        # draw text
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
                txt_kwargs['center'] = tw // 2, th // 2
            elif self.txt_positioning == 'topleft':
                txt_kwargs['pos'] = 0, 0 
            ptext.draw(self._txt, **txt_kwargs)
        surf.set_colorkey(TRANSPARENT, pg.RLEACCEL)
        surf.convert()
        self.image = surf
        self.dirty = 1
        self.recompute = 0
    
    def set_txt(self, txt):
        if txt != self._txt:
            self._txt = txt
            self._recompute()
    
    def set_shapes(self, shapes):
        self.shapes = shapes
        self._recompute()
        
    def update(self, *args, **kwargs):
        if self.recompute or pview.size != self._res:
            self._recompute()
