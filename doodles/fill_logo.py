import os

from PIL import Image  # Pillow >= 1.0 does not support import Image.

import pygame as pg 


# utils from https://github.com/cosmologicon/maff/blob/master/maff.py
def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0
def clamp(x, a, b):
    return a if x < a else b if x > b else x


def color_from_alignment(g, l):
    """ return 3-tuple from goodness g and lawfulness l. 
    good = bright, evil = dark, lawful = blue, chaotic = red.
    g and l range from -50 to +50.
    """
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


def load_image(img_path, colorkey=None):
    """ load image from disk. Return Surface. """
    img = pg.image.load(img_path).convert()
    if colorkey:
        img.set_colorkey(colorkey, pg.RLEACCEL)
    return img 

def make_silhouette(img_path, output_path, dest_size=(64, 64)):
    """ convert image to binary (ie to black and white without antialias).
    img_path: filepath of input image.
    output_path: file to save to.
    dest_size: 2-tuple, size of destination image. 
    If resolution of original img is not dest_size, pad with white 
    and preserve original resolution.
    Return Surface where background color is white and silhouette color black.
    """
    tmp_filepath = 'tmp_conv_binary.png'
    if not output_path:
        output_path = tmp_filepath
    with Image.open(img_path) as img_file: 
        img_file = img_file.convert('1', dither=Image.FLOYDSTEINBERG)
        img_file.save(output_path)
    # scale 4x then shrink to smooth rough contours left by binarizing antialias 
    img = load_image(output_path)
    w0, h0 = img.get_size()
    img = pg.transform.scale2x(img)
    img = pg.transform.scale2x(img)
    # shrink to fit on dest surface
    w, h = dest_size
    dest_surf = pg.Surface((w, h))
    dest_surf.fill((255, 255, 255))
    if w0 > h0:
        img = pg.transform.scale(img, (w, w * h0 // w0))
    else:
        img = pg.transform.scale(img, (h * w0 // h0, h))
    blit_rect = img.get_rect(center=dest_surf.get_rect().center)
    dest_surf.blit(img, blit_rect)
    pg.image.save(dest_surf, output_path)
    if output_path == tmp_filepath:
        os.remove(output_path)
    return dest_surf

def make_avatar1(bin_img, goodness, lawfulness):
    """ bin_img is a binary image (ie black and white).
    g = goodness, -50 to 50
    l = lawfulness, -50 to 50
    Return image where bg color is shade of purple and foreground is silhouette.
    """
    dest_surf = pg.Surface(bin_img.get_size())
    dest_surf.fill(color_from_alignment(goodness, lawfulness))
    img = bin_img.copy()
    img.set_colorkey((255, 255, 255), pg.RLEACCEL)
    dest_surf.blit(img, (0, 0))
    return dest_surf

def main():
    pg.init()
    w, h = 800, 600
    pg.display.set_mode((w, h))
    screen = pg.display.get_surface()
    screen.fill((55, 55, 55))
    # convert image to square monochrome silhouette, and store it to other file
    sil_img = make_silhouette('owl3.png', 'owl3_mono.png')
    n = 3  # number of colors displayed on each side of the spectrum 
    for i in range(n * 2 + 1):
        for j in range(n * 2 + 1):
            ww, hh = w // (n * 2 + 1), h // (n * 2 + 1)
            rect = 10 + i * ww, 10 + j * hh, ww - 2, hh - 2
            goodness = j * 100 // n // 2 - 50
            lawfulness = i * 100 // n // 2 - 50
            img = make_avatar1(sil_img, goodness, lawfulness)
#             img = make_avatar2(sil_img, goodness, lawfulness)
            screen.blit(img, rect)
            
    # flip screen
    pg.display.flip()
    # dummy run
    clock = pg.time.Clock()
    while not pg.event.peek([pg.QUIT, pg.KEYDOWN]):
        clock.tick(30)        
        

if __name__ == "__main__":
    main()
