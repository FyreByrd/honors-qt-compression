from quad_tree_compression import compress_image_file, reconstruct_image_from_file
from os.path import getsize

#name = "StoneTile"

files = [
    "test",
    "Curvature",
    "Dragon",
    "HighRappel",
    "Room",
    "stone",
    "StoneTile",
    "test3",
    "worst-square64"
]

for name in files:
    try:
        print(name)
        # Compress the image and encode is a binary file (any file extension can be chosen)
        dims = compress_image_file("input/"+name+".png", "output/"+name+"_qt.qid", iterations=50_000)
        print(" dim: "+str(dims))
        raw = dims[0]*dims[1]*dims[2]
        print(" raw: "+str(raw))
        cmp = getsize("output/"+name+"_qt.qid")
        print(" cmp: "+str(cmp))
        png = getsize("input/"+name+".png")
        print(" png: "+str(png))
        print(" cmp/raw: "+str(cmp / raw))
        print(" cmp/png: "+str(cmp / png))

        # Reconstruct the image from the binary file. (Returns a PIL.Image object)
        image = reconstruct_image_from_file("output/"+name+"_qt.qid")
        image.save("output/"+name+".png")
    except ValueError as ve:
        print(ve)