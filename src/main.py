from controls import controller
import pygame as pg
from scene_manager import scene_manager
import settings


pg.init()
pg.display.set_mode((800, 600))
clock = pg.time.Clock()


while True:
    ms = clock.tick(settings.FPS)
    if controller.poll():
        break
    scene_manager.tick(ms)
    pg.display.flip() # render
