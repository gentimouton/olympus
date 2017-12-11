from constants import OUT_FSCR, OUT_QUIT
from controls import controller
import pview
import pygame as pg
from scene_manager import scene_manager
import settings


def main():
    pg.init()
    pg.display.set_caption('Olympus')
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    
    while True:
        ms = clock.tick(settings.FPS) # throttle
        
        outcome = controller.poll() # get player input
        if outcome == OUT_QUIT:
            break

        outcome = scene_manager.tick(ms) # update scene 
        if outcome == OUT_FSCR:
            scene_manager.refresh_view()
        if outcome == OUT_QUIT:
            break
        
        pg.display.flip()  # render

if __name__ == "__main__":
    main()
