import pview
import pygame as pg
import settings


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
        quitme = False
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
                quitme = True
            if event.type == pg.KEYDOWN:
                if event.key in valid_keys:
                    self._bdown_events.add(kmap[event.key])
                if event.key == pg.K_ESCAPE:
                    quitme = True
                if event.key == pg.K_F11:
                    pview.toggle_fullscreen() 
                if event.key == pg.K_F4 and alt_held:
                    quitme = True
        return quitme 
    
    def btn_ispressed(self, btn):
        return btn in self._bpressed
    
    def btn_event(self, btn):
        return btn in self._bdown_events
    

controller = Controller()