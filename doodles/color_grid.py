import pygame as pg

# utils from https://github.com/cosmologicon/maff/blob/master/maff.py
def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0
def clamp(x, a, b):
    return a if x < a else b if x > b else x


def color_from_alignment(g, l):
    """ g and l range from -50 to +50 """
    maxv = 200
    midv = 130
    minv = 80
    g, l = clamp(g, -50, 50), clamp(l, -50, 50) 
    if sign(g) < 1:  # evil or neutral
        sat = minv + (maxv - minv) * (g + 50) // 50  # minv to maxv
        if sign(l) < 1:  # chaotic or neutral
            color = sat, 0, sat * (l + 50) // 50
        else:  # lawful
            color = sat * (50 - l) // 50, 0, sat
    else:  # good
        sat = midv * g // 50
        if sign(l) < 1:  # chaotic or neutral 
            color = maxv, sat, sat + (maxv - sat) * (l + 50) // 50
        else: 
            color = sat + (maxv - sat) * (50 - l) // 50, sat, maxv 
    # color = clamp(color[0], 0, 255), clamp(color[1], 0, 255), clamp(color[2], 0, 255)
    return color
    
# 400 - 402 - 404 - 204 - 004   evil
# a00 - a05 - a0a - 50a - 00a
# f00 - f08 - f0f - 80f - 00f
# f55 - f5a - f5f - a5f - 55f
# faa - fac - faf - caf - aaf   good
# chaos                order

def main():
    pg.init()
    w, h = 800, 600
    pg.display.set_mode((w, h))
    screen = pg.display.get_surface()
    # draw stuff
    n = 5  # number of colors displayed on each side of the spectrum 
    for i in range(n * 2 + 1):
        for j in range(n * 2 + 1):
            ww, hh = w // (n * 2 + 1), h // (n * 2 + 1)
            rect = 2 + i * ww, 2 + j * hh, ww - 2, hh - 2
            color = color_from_alignment(j * 100 // n // 2 - 50, i * 100 // n // 2 - 50)
            screen.fill(color, rect)
    pg.display.flip()
    # dummy run
    clock = pg.time.Clock()
    while not pg.event.peek([pg.QUIT, pg.KEYDOWN]):
        clock.tick(30)        
        

if __name__ == "__main__":
    main()

