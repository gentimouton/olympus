from controls import controller
import pview
import pygame as pg
from scene_manager import scene_manager
import settings


def main():
    pg.init()
    pg.display.set_caption('Olympus')
    pg.font.init()
    pview.set_mode((800, 600))
    clock = pg.time.Clock()
    
    
    while True:
        ms = clock.tick(settings.FPS)
        if controller.poll():  # returns True if game should stop
            break
        if scene_manager.tick(ms):  # returns True if game should stop 
            break
        pg.display.flip()  # render

if __name__ == "__main__":
    main()
