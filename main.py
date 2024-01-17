#!/usr/bin/python3
from PIL import Image
from numpy import asarray
from quad_image import quad_image, child_indices, size

if __name__=="__main__":
    img = Image.open("test.png")

    npdata = asarray(img)

    qi = quad_image(npdata)

    qi.write_file("test.png.qi")

    qi.compress()

    qi.write_file("test-c.png.qi")

    exit()
    q2 = quad_image()
    q2.read_file("test-c.png.qi")

    q2.decompress()
    nd2 = q2.get_channels()

    pi = Image.fromarray(nd2)
    pi.save("test-s.png")