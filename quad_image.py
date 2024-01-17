import numpy as np
from math import log2, floor
from functools import reduce

def p2(a: int) -> int:
    b = log2(a)
    c = floor(b)
    return c if b.is_integer() else c + 1

def depth(x: int, y: int) -> int:
    return max(p2(x), p2(y))

def size(levels: int) -> int:
    return (1 - 4 ** (levels + 1)) // (-3)

def child_indices(p: int, l: int):
    #return [i for i in range(4*p + 1, 4*p + 5)]
    o = 2**l
    i = p - size(l - 1)
    j = i + size(l)
    j += (i % o)
    j += (2*l + 2**(l+1)) * (i//o)

    return (j, j+1, j + 2**(l+1), j + 2**(l+1) + 1)

class quad_image:
    def __init__(this, arr: np.ndarray=np.ndarray((0,0,0)), threshold: int=0):
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
                        this.channels[c][fill + x * this.x + y] = this.channels[c][fill + x * this.x + y - 1]#0
                    else:
                        this.channels[c][fill + x * this.x + y] = arr[x][y][c]
            this.ch_flags[c][1 + fill//8:] = 0xff
            this.ch_flags[c][fill//8] |= 0xff >> fill % 8
            this.ch_flags[c][this.size//8] &= 0xff << 8 * this.ch_flags.shape[1] - this.size
        this.threshold = threshold

    def isleaf(this, ch, ni):
        return ni < this.size and (this.ch_flags[ch][ni//8] & 0x80 >> ni%8) != 0
    
    def flip(this, ch, ni):
        this.ch_flags[ch][ni//8] ^= 0x80 >> ni%8

    def cmp_help(this, ch: int, ri: int, lev: int):
        if ri >= this.size:
            return ri
        children = child_indices(ri, lev)
        for c in children:
            this.cmp_help(ch, c, lev + 1)
        for c in children:
            if not this.isleaf(ch, c):
                return ri
        avg = 0
        for c in children:
            avg += this.channels[ch][c]
        avg //= 4
        for c in children:
            if abs(avg - this.channels[ch][c]) > this.threshold:
                return ri
        this.channels[ch][ri] = avg
        this.flip(ch, ri)
        for c in children:
            this.flip(ch, c)
        return ri

    def compress(this):
        for c in range(this.channels.shape[0]):
            #print("before: ")
            #print(this.ch_flags[c])
            #print(list(this.channels[c]))
            this.cmp_help(c, 0, 0)
            #print("after:")
            #print(this.ch_flags[c])
            #print(list(this.channels[c]))

    def dcp_help(this, ch: int, ri: int, lev: int):
        children = child_indices(ri, lev)
        if ri >= this.size or children[0] >= this.size:
            return ri
        if this.isleaf(ch, ri):
            this.flip(ch, ri)
            for c in children:
                this.channels[ch][c] = this.channels[ch][ri]
                this.flip(ch, c)
        for c in children:
            this.dcp_help(ch, c, lev + 1)
        return ri

    def decompress(this):
        for c in range(this.channels.shape[0]):
            this.dcp_help(c, 0, 0)

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
                for i in range(this.size):
                    if i % 8 == 0:
                        this.ch_flags[c][i//8] = data[start]
                        start += 1
                    if this.isleaf(c, i):
                        this.channels[c][i] = data[start]
                        start += 1

    def write_file(this, fname: str):
        with open(fname, "wb") as f:
            f.write(this.w.to_bytes(4, 'little'))
            f.write(this.h.to_bytes(4, 'little'))
            f.write(this.channels.shape[0].to_bytes(1))
            for c in range(this.channels.shape[0]):
                i = 0
                while i < this.size:
                    if i % 8 == 0:
                        f.write(this.ch_flags[c][i//8])
                    if this.isleaf(c, i):
                        f.write(np.uint8(this.channels[c][i]))
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
