import pygame as pg

FPS = 30
DEBUG = True

# map button to keys
bmap = {
    'select': [pg.K_SPACE, pg.K_RETURN],
    'up': [pg.K_UP, pg.K_w],
    'down': [pg.K_DOWN, pg.K_s],
    'left': [pg.K_LEFT, pg.K_a],
    'right': [pg.K_RIGHT, pg.K_d]
    }

# map keys to button, eg K_d -> 'right'
kmap = {e: btn for (btn, v) in bmap.items() for e in v} 
