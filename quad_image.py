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
    def __init__(this, arr: np.ndarray=np.ndarray((0,0,0))):
        dims = arr.shape
        if dims[0] <= 0:
            return
        this.w = dims[0] #actual width of image
        this.h = dims[1] #actual height of image
        this.depth = depth(this.w, this.h) #depth of tree
        this.size = size(this.depth) #size of tree
        this.x = 2**this.depth #adjusted width of image for compression
        this.channels = np.ndarray((dims[2], this.size), np.uint8) #array of sequential quadtrees
        this.ch_flags = np.zeros((dims[2], 1 + this.size // 8), dtype=np.uint8) #bit flags of node vs leaf for compression
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
            this.ch_flags[c][1 + fill//8:] = 0xff
            this.ch_flags[c][fill//8] |= 0xff >> fill % 8
            this.ch_flags[c][this.size//8] &= 0xff << 8 * this.ch_flags.shape[1] - this.size

    def compress(this):
        pass

    def decompress(this):
        pass

    def read_file(this, fname: str):
        with open(fname, "rb") as f:
            data = np.fromfile(f, dtype=np.uint8)
            this.w = int.from_bytes(data[0:4], 'little')
            this.h = int.from_bytes(data[4:8], 'little')
            this.depth = depth(this.w, this.h) #depth of tree
            this.size = size(this.depth) #size of tree
            this.x = 2**this.depth #adjusted width of image for compression
            ch = data[8]
            this.channels = np.zeros((ch, this.size), dtype=np.uint8) #array of sequential quadtrees
            this.ch_flags = np.zeros((ch, 1 + this.size // 8), dtype=np.uint8) #bit flags of node vs leaf for compression
            start = 9
            for c in range(ch):
                bits = data[start]
                for i in range(this.size):
                    if i % 8 == 0:
                        bits = data[start]
                        this.ch_flags[c][i//8] = bits
                        start += 1
                    if (bits & (0x80 >> i % 8)) != 0:
                        this.channels[c][i] = data[start]
                        start += 1

    def write_file(this, fname: str):
        with open(fname, "wb") as f:
            f.write(this.w.to_bytes(4, 'little'))
            f.write(this.h.to_bytes(4, 'little'))
            f.write(this.channels.shape[0].to_bytes(1))
            for c in range(this.channels.shape[0]):
                bits = np.uint8(this.ch_flags[c][0])
                i = 0
                while i < this.size:
                    if i % 8 == 0:
                        f.write(bits)
                    if (bits & (0x80 >> i % 8)) != 0:
                        f.write(np.uint8(this.channels[c][i]))
                    if i % 8 == 7:
                        bits = this.ch_flags[c][1 + i//8]
                    i += 1

    def get_channels(this):
        ret = np.ndarray((this.w, this.h, this.channels.shape[0]), np.uint8)
        dims = ret.shape
        mi = this.size - this.x ** 2
        for c in range(dims[2]):
            for x in range(this.x):
                for y in range(this.x):
                    if x < this.w and y < this.h:
                        ret[x][y][c] = this.channels[c][mi + x * this.x + y]
        return ret
