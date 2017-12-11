import pygame as pg
import settings


class Controller():
    def __init__(self):
        self._bdowns = set()  # buttons down this frame. maybe pressed earlier.
        self._bpressed = set()  # buttons newly pressed this frame
    
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
        # keys that were pressed this frame, might overlap with keys pressed
        self._bdowns = set()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quitme = True
            if event.type == pg.KEYDOWN:
                if event.key in valid_keys:
                    self._bdowns.add(kmap[event.key])
                if event.key == pg.K_ESCAPE:
                    quitme = True
                if event.key == pg.K_F11:
                    print('TODO: full screen') 
                if event.key == pg.K_F4 and alt_held:
                    quitme = True
        return quitme 
    
    def btn_ispressed(self, btn):
        return btn in self._bpressed
    
    def btn_isdown(self, btn):
        return btn in self._bdowns
    

controller = Controller()