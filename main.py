#!/usr/bin/python3
from PIL import Image
from numpy import asarray
from quad_image import quad_image

if __name__=="__main__":
    img = Image.open("test.png")

    npdata = asarray(img)

    qi = quad_image(npdata)

    qi.write_file("test.png.qi")

    q2 = quad_image()
    q2.read_file("test.png.qi")

    nd2 = q2.get_channels()

    pi = Image.fromarray(nd2)
    pi.save("s-test.png")