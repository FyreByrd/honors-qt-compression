#!/usr/bin/python3
from PIL import Image
from numpy import asarray
from quad_image import quad_image

if __name__=="__main__":
    img = Image.open("test.png")

    npdata = asarray(img)

    qi = quad_image(npdata)
