import numpy as np
from math import log2, floor

def p2(a: int) -> int:
    b = log2(a)
    c = floor(b)
    return c if b.is_integer() else c + 1

def depth(x: int, y: int) -> int:
    return max(p2(x), p2(y))

def size(levels: int) -> int:
    return (1 - 4 ** (levels + 1)) // (-3)

class quad_image:
    def __init__(this, arr: np.ndarray):
        dims = arr.shape
        this.w = dims[0] #actual width of image
        this.h = dims[1] #actual height of image
        this.depth = depth(this.w, this.h) #depth of tree
        this.size = size(this.depth) #size of tree
        this.x = 2**this.depth #adjusted width of image for compression
        this.channels = np.ndarray((dims[2], this.size), int) #array of sequential quadtrees
        this.ch_flags = [bytearray()]*dims[2] #bit flags of node vs leaf for compression
        fill = this.size - this.x ** 2
        for c in range(dims[2]):
            for i in range(fill):
                this.channels[c][i] = 0
            for x in range(this.x):
                for y in range(this.x):
                    if x >= this.w or y >= this.h:
                        this.channels[c][fill + x * this.x + y] = 0
                    else:
                        this.channels[c][fill + x * this.x + y] = arr[x][y][c]

    def compress(this):
        pass

    def decompress(this):
        pass

    def read_file(this, fname: str):
        pass

    def write_file(this, fname: str):
        pass
                
                
