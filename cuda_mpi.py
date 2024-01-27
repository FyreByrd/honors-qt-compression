from mpi4py import MPI

from quad_tree_compression import compress_and_encode_image_data, reconstruct_image_data
from os.path import getsize
from time import time
from math import sqrt

from PIL import Image
import cupy as cp

comm = MPI.COMM_WORLD
rank = int(comm.Get_rank())
size = int(comm.Get_size())

if int(sqrt(size))**2 != size:
    if rank == 0:
        print("Error: number of processes must be a square number")
        exit(1)
    exit()

#mpiexec -n 4 python3 mpi.py
    
def chunk_i(h: int, w: int):
    sz = int(sqrt(size))
    x, y, z, v = 0,0,0,0

    x = (h // sz) * (rank // sz)
    y = x + h // sz

    if (rank // sz) % sz == sz - 1:
        y = h

    z = (w // sz) * (rank % sz)
    v = z + w // sz

    if rank % sz == sz - 1:
        v = w
    
    return (x,y,z,v)

def compress_image_file(
        image_path: str,
        output_path: str,
        iterations: int = 20000,
        detail_error_threshold: float = 10):
    image_data = None
    dims = None
    if rank == 0:
        image = Image.open(image_path)
        image_data = cp.array(image)
        dims = image_data.shape
    
    dims = comm.bcast(dims, root=0)
    if rank != 0:
        image_data = cp.empty(dims, cp.uint8)
    comm.Bcast(image_data, root=0)

    inds = chunk_i(dims[0], dims[1])

    chunk = compress_and_encode_image_data(cp.array(image_data[inds[0]:inds[1],inds[2]:inds[3], :]), iterations // size, detail_error_threshold)

    chunks = comm.gather((rank, chunk), root=0)

    if rank == 0:
        with open(output_path, "wb") as file:
            file.write(size.to_bytes(2, "little"))
            for i in range(size):
                file.write(chunks[i][0].to_bytes(2, "little"))
                file.write(len(chunks[i][1]).to_bytes(4, "little"))
                file.write(chunks[i][1])

    #return dimensions
    return dims

def reconstruct_image_from_file(compressed_image_file: str) -> Image:
    data = None
    sz = 0
    if rank == 0:
        with open(compressed_image_file, "rb") as file:
            data = file.read()
        sz = int(sqrt(int.from_bytes(data[0:2], "little")))

    si = 2
    sz = comm.bcast(sz, root=0)
    data = comm.bcast(data, root=0)
    l = 0
    c = 0
    for i in range(sz**2):
        c = int.from_bytes(data[si:si+2], "little")
        si += 2
        l = int.from_bytes(data[si:si+4], "little")
        si += 4
        if rank == c:
            break
        si += l
    chunk = reconstruct_image_data(data[si:si+l])
    chunks = comm.gather((c, chunk))
    if rank == 0:
        chunks = list(map(lambda c: c[1], sorted(chunks, key=lambda c: c[0])))
        tmp = []
        for i in range(sz):
            tmp.append(cp.hstack(chunks[i*sz:(i+1)*sz]))
        image_data = cp.asnumpy(cp.vstack(tmp))

        return Image.fromarray(image_data)

#name = "StoneTile"

files = [
    "splotches.png",
    "cooper.jpg",
    "door.jpg",
    #"dragon.png",
    #"hills.png",
    #"mountains.png",
    "room.png",
    #"sandwich.jpg",
    #"science.jpg",
    #"tree.jpg",
    #"worst-square.png"
]

results = None
if rank == 0:
    results = open("results-mpi-cuda.csv", "w")
    results.write("file,ct,h,w,raw,cmp,og,cmp/raw,cmp/og,rt\n")

for file in files:
    try:
        l = None
        if rank == 0:
            print(file)
            l = file
        name = ".".join(file.split(".")[:-1])
        # Compress the image and encode is a binary file (any file extension can be chosen)
        t = time()
        dims = compress_image_file("input/"+file, "output-c-m/"+name+"_qt.qid", iterations=64_000)
        if rank == 0:
            l += ","+str(time() - t)
            l += ","+str(dims[0])+","+str(dims[1])
            raw = dims[0]*dims[1]*dims[2]
            l += ","+str(raw)
            cmp = getsize("output-c-m/"+name+"_qt.qid")
            l += ","+str(cmp)
            og = getsize("input/"+file)
            l += ","+str(og)+","+str(cmp / raw)+","+str(cmp / og)
            # Reconstruct the image from the binary file. (Returns a PIL.Image object)
            t = time()
        image = reconstruct_image_from_file("output-c-m/"+name+"_qt.qid")
        if rank == 0:
            l += ","+str(time() - t)
            image.save("output-c-m/"+file)
            results.write(l+"\n")
    except ValueError as ve:
        print(ve)
if rank == 0:
    results.close()