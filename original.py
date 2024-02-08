from quad_image import quad_image
from os.path import getsize
from time import time

from PIL import Image
import numpy as np

def compress_image_file(
        image_path: str,
        output_path: str):

    image = Image.open(image_path)
    image_data = np.array(image)

    dims = image_data.shape

    qi = quad_image(image_data)
    qi.compress()
    qi.write_file(output_path)

    #return dimensions
    return dims

def reconstruct_image_from_file(compressed_image_file: str) -> Image:
    qi = quad_image()
    qi.read_file(compressed_image_file)
    qi.decompress()

    image_data = qi.get_channels()
    return Image.fromarray(image_data)

files = [
    "64/barnacles.png",
    "64/cooper.png",
    "64/door.png",
    "64/science.png",
    "64/tree.png",
    "256/barnacles.png",
    "256/cooper.png",
    "256/door.png",
    "256/science.png",
    "256/tree.png",
    "1024/barnacles.png",
    "1024/cooper.png",
    "1024/door.png",
    "1024/science.png",
    "1024/tree.png"
]

results = open("results-original.csv", "w")
results.write("file,ct,h,w,raw,cmp,og,cmp/raw,cmp/og,rt\n")

for file in files:
    try:
        print(file)
        l = file
        name = ".".join(file.split(".")[:-1])
        # Compress the image and encode is a binary file (any file extension can be chosen)
        t = time()
        dims = compress_image_file("input/"+file, "output-s/"+name+"_qt.qid")
        l += ","+str(time() - t)
        l += ","+str(dims[0])+","+str(dims[1])
        raw = dims[0]*dims[1]*dims[2]
        l += ","+str(raw)
        cmp = getsize("output-s/"+name+"_qt.qid")
        l += ","+str(cmp)
        og = getsize("input/"+file)
        l += ","+str(og)+","+str(cmp / raw)+","+str(cmp / og)

        # Reconstruct the image from the binary file. (Returns a PIL.Image object)
        t = time()
        image = reconstruct_image_from_file("output-s/"+name+"_qt.qid")
        l += ","+str(time() - t)
        image.save("output-s/"+file)
        results.write(l+"\n")
    except ValueError as ve:
        print(ve)
results.close()