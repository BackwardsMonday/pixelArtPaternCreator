import math
from PIL import Image
from PIL import ImageDraw 
from PIL import ImageFont
import pprint

def colorDistance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt(((r2-r1)*0.3)**2 + ((g2-g1)*0.59)**2 + ((b2-b1)*0.11)**2)

def quantizeToPalette(silf, palette, dither=False):
    """Convert an RGB or L mode image to use a given P image's palette."""

    silf.load()

    # use palette from reference image
    palette.load()
    if palette.mode != "P":
        raise ValueError("bad mode for palette image")
    if silf.mode != "RGB" and silf.mode != "L":
        raise ValueError(
            "only RGB or L mode images can be quantized to a palette"
            )
    im = silf.im.convert("P", 1 if dither else 0, palette.im)
    # the 0 above means turn OFF dithering

    # Later versions of Pillow (4.x) rename _makeself to _new
    try:
        return silf._new(im)
    except AttributeError:
        return silf._makeself(im)
    
def pixilizeImage(convertedImage, palette, pixelSize, changeBkg = True, bkgColor = (255,255,255), grayThreshold = 100, gray = (149,145,140)):
    #convert image diminsions to be divisible by pixel size
    convertedImage = convertedImage.resize((int(convertedImage.size[0]/pixelSize), int(convertedImage.size[1]/pixelSize)), Image.NEAREST)
    convertedImage = convertedImage.resize((int(convertedImage.size[0]*pixelSize), int(convertedImage.size[1]*pixelSize)), Image.NEAREST)

    pixel = convertedImage.load()
    for i in range(0, convertedImage.size[0], pixelSize):
        for j in range(0, convertedImage.size[1], pixelSize):
            color = pixel[i+(pixelSize/4), j+(pixelSize/4)]

            #change background if the pixel if white or off white
            if changeBkg and color[0] > 240 and color[1] > 240 and color[2] > 240:
                setColor = bkgColor
            
            #next thing dislikes greys so deal with them first
            #TODO: if possibile eventualy adapt this to allow for multipule grays
            elif color[0] == color[1] and color[1] == color[2]:
                if color[0] < grayThreshold:
                    setColor=(0,0,0)
                elif color[0] < 200:
                    setColor=gray
                else:
                    setColor=(255,255,255)
            else:
                palette_r = palette[::3]
                palette_g = palette[1::3]
                palette_b = palette[2::3]
                palette_rgb = zip(palette_r,palette_g,palette_b)
                closest_colors = sorted(palette_rgb, key=lambda palette_color: colorDistance(color, palette_color))
                setColor =  closest_colors[0]
            for x in range(pixelSize):
                for y in range(pixelSize):
                    pixel[i+x,j+y] = setColor
    return convertedImage

            
            