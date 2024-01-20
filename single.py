from quad_tree_compression import compress_image_file, reconstruct_image_from_file
from os.path import getsize
from time import time

#name = "StoneTile"

files = [
    "cooper.jpg",
    "door.jpg",
    "dragon.png",
    "hills.png",
    "mountains.png",
    "room.png",
    "sandwich.jpg",
    "science.jpg",
    "splotches.png",
    "tree.jpg",
    "worst-square.png"
]

results = open("results.csv", "w")
results.write("file,ct,h,w,raw,cmp,og,cmp/raw,cmp/og,rt\n")

for file in files:
    try:
        print(file)
        l = file
        name = ".".join(file.split(".")[:-1])
        # Compress the image and encode is a binary file (any file extension can be chosen)
        t = time()
        dims = compress_image_file("input/"+file, "output/"+name+"_qt.qid", iterations=64_000)
        l += ","+str(time() - t)
        l += ","+str(dims[0])+","+str(dims[1])
        raw = dims[0]*dims[1]*dims[2]
        l += ","+str(raw)
        cmp = getsize("output/"+name+"_qt.qid")
        l += ","+str(cmp)
        og = getsize("input/"+file)
        l += ","+str(og)+","+str(cmp / raw)+","+str(cmp / og)

        # Reconstruct the image from the binary file. (Returns a PIL.Image object)
        t = time()
        image = reconstruct_image_from_file("output/"+name+"_qt.qid")
        l += ","+str(time() - t)
        image.save("output/"+file)
        results.write(l+"\n")
    except ValueError as ve:
        print(ve)
results.close()