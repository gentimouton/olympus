import pview
import pygame as pg
import settings
from constants import OUT_FSCR, OUT_NONE, OUT_QUIT

class Controller():
    def __init__(self):
        self._bdown_events = set()  # buttons newly pressed this frame
        self._bpressed = set()  # buttons still pressed right now.
    
    def poll(self):
        """ 
        toggle fullscreen with F11, 
        quit with ESC or alt-F4. 
        returns whether the program should stop 
        """
        kmap = settings.kmap
        valid_keys = settings.kmap.keys()
        # keys being down
        kpressed = pg.key.get_pressed()
        alt_held = kpressed[pg.K_LALT] or kpressed[pg.K_RALT]
        self._bpressed = set([kmap[k] for k in valid_keys if kpressed[k]])
        # keys that were pressed just now. Also included in kpressed.
        self._bdown_events = set()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return OUT_QUIT
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return OUT_QUIT
                elif event.key == pg.K_F4 and alt_held:
                    return OUT_QUIT
                elif event.key in valid_keys:
                    self._bdown_events.add(kmap[event.key])
                elif event.key == pg.K_F11:
                    pview.toggle_fullscreen()
                    return OUT_FSCR
        return OUT_NONE
    
    def btn_ispressed(self, btn):
        return btn in self._bpressed
    
    def btn_event(self, btn):
        return btn in self._bdown_events
    

controller = Controller()