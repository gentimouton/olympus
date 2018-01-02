import pygame as pg


TRANSPARENT = 255, 0, 255
PI = 3.14159
SQRT2 = 1.414

def make_emoji(goodness, color1=(0, 0, 0), color2=TRANSPARENT):
    """ Draw an emoji face reflecting alignment. 
    goodness ranges from -50 (evil) to +50 (good). 0 is neutral.
    Return surface.
    """
    surf = pg.Surface((128, 128))
    surf.set_colorkey(TRANSPARENT, pg.RLEACCEL)
    surf.fill((255, 0, 255))
    pg.draw.circle(surf, color1, (64, 64), 64)  # face
#     surf.fill((color1))
    pg.draw.circle(surf, color2, (40, 48), 10)  # left eye
    pg.draw.circle(surf, color2, (88, 48), 10)  # right eye
    if goodness < 0:  # eye covers
        d = 5 + 15 * abs(goodness) // 50  # triangle width and height
        pg.draw.polygon(surf, color1, [(30, 38), (30 + d, 38), (30, 38 + d)])
        pg.draw.polygon(surf, color1, [(98, 38), (98 - d, 38), (98, 38 + d)])
#         pg.draw.circle(surf, color1, (30, 38), d)
#         pg.draw.circle(surf, color1, (98, 38), d)
    if goodness > 0:  # eye covers
        d = 5 * abs(goodness) // 50
        pg.draw.circle(surf, color1, (40, 58 - d), 10)
        pg.draw.circle(surf, color1, (88, 58 - d), 10)
    if goodness < 0:  # evil imp ears
        d = int((1 - SQRT2 / 2) * 64 - 12 * abs(goodness) // 50) 
        pg.draw.polygon(surf, color1, [(d, d), (48, d + 5), (d + 5, 48)])
        pg.draw.polygon(surf, color1, [(128 - d, d), (128 - 48, d + 5), (128 - d - 5, 128 - 48)])

    dx = abs(16 * goodness // 50)  # from 16 (good) to 0 (neutral) to 16 (evil)
    dy = abs(16 * goodness // 50)  # from 16 (good) to -16 (evil)
    
    points = [(48 - dx, 88 - dy), (48, 88 - 5), (80, 88 - 5),
              (80 + dx, 88 - dy), (80, 88 + 5), (48, 88 + 5)]
    pg.draw.polygon(surf, color2, points, 0)
    return surf
    
def main():
    pg.init()
    pg.display.set_mode((800, 600))
    screen = pg.display.get_surface()
    screen.fill((222, 222, 55))
    n = 2  # number of samples displayed on each side of the goodness scale 
    for i in range(n * 2 + 1):
        goodness = i * 100 // n // 2 - 50
        img = make_emoji(goodness)
        screen.blit(img, (10 + i * 140, 200))
    pg.display.flip()
    clock = pg.time.Clock()
    while not pg.event.peek([pg.QUIT, pg.KEYDOWN]):
        clock.tick(30)
        

if __name__ == "__main__":
    main()
