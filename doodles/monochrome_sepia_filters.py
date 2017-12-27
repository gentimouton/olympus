import pygame as pg
import time
from PIL import Image  # Pillow >= 1.0 does not support import Image.
import numpy as np
    
def gray_scale(img_path):
    """ convert image to grayscale """
    img = pg.image.load(img_path).convert()
    start_time = time.time()
    arr = pg.surfarray.array3d(img)
    # https://stackoverflow.com/a/10693616
    # photoshop luminosity filter: 298,587,114, ie ITU-R_BT.601_conversion
    # luminance: 213, 715, 072 https://en.wikipedia.org/wiki/Relative_luminance
#     avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in arr]
#     arr = np.array([[[avg, avg, avg] for avg in col] for col in avgs]) # slow
    arr = arr.dot([0.298, 0.587, 0.114])[:, :, None].repeat(3, axis=2)  # fast
    print('surface grayscaling took %.2fs' % (time.time() - start_time))
    return pg.surfarray.make_surface(arr)

def load_image(img_path, colorkey=None):
    """ convert image to grayscale """
    img = pg.image.load(img_path).convert()
    if colorkey is not None:
        img.set_colorkey(colorkey, pg.RLEACCEL)
    return img 


def sepia_filter(img_path):
    """ pass img through sepia filter and return surface.
    Does not work (ValueError) on black and white images.
    """
    img = pg.image.load(img_path).convert()
    arr = pg.surfarray.array3d(img)
    # https://stackoverflow.com/a/23806249
    sepia_filter = np.array([[.393, .769, .189],
                             [.349, .686, .168],
                             [.272, .534, .131]])
    arr = arr.dot(sepia_filter.T)
    arr = np.clip(arr, 0, 255) # cap at 255
    return pg.surfarray.make_surface(arr)
    
def main():
    pg.init()
    pg.display.set_mode((800, 600))
    screen = pg.display.get_surface()
    screen.fill((55, 55, 111))
    # sepia_filter on landscape
    img = sepia_filter('landscape.png')
    screen.blit(img, (100, 100))
    # monoscale a quasi-monoscale image (eg black and white with antialias)
    with Image.open("owl1_antialiased.png") as img_file: 
        # PIL is a shit show https://stackoverflow.com/a/12646282
        img_file = img_file.convert('1', dither=Image.FLOYDSTEINBERG)  # convert image to black and white
        img_file.save('owl1_mono.png')
    # display it
    img = load_image('owl1_mono.png', (255, 255, 255))
    screen.blit(img, (100, 100))
    # display smaller version
    w, h = img.get_rect().size
    img = pg.transform.scale(img, (100, h * 100 // w))
    screen.blit(img, (500, 350))
    # flip screen    
    pg.display.flip()
    # dummy run
    clock = pg.time.Clock()
    while not pg.event.peek([pg.QUIT, pg.KEYDOWN]):
        clock.tick(30)        
        

if __name__ == "__main__":
    main()

