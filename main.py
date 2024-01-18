#!/usr/bin/python3
from PIL import Image
from numpy import asarray
from quad_image import quad_image, child_indices, size
from os.path import getsize
from os import remove
from time import time

def test_many():
    files = [
        "test-images/test.png",
        "test-images/ball.png",
        "test-images/Basketball.png",
        "test-images/Curvature.png",
        #"test-images/Dragon.png",
        "test-images/HighRappel.png",
        "test-images/Room.png",
        "test-images/stone.png",
        "test-images/StoneTile.png",
        "test-images/test2.png",
        "test-images/test3.png",
        "test-images/worst-square4.png",
        "test-images/worst-square64.png"
    ]

    thresholds = [0,1,2,4,8,16,32,64]

    for th in thresholds:
        print("threshold: "+str(th))
        for f in files:
            print(f)
            img = Image.open(f)
            png = getsize(f)
            npdata = asarray(img)
            print(" dimensions: "+str(npdata.shape))
            print(" PNG       : "+str(png)+" bytes")
            dims = npdata.shape
            raw = dims[0] * dims[1] * dims[2]
            print(" raw       : "+str(raw)+" bytes")
            t = time()
            qi = quad_image(npdata, th)
            print(" construct : "+str(time() - t))
            t = time()
            qi.write_file("aaa")
            print(" file      : "+str(time() - t))
            qf = getsize("aaa")
            print(" quad-image: "+str(qf)+" bytes")
            
            t = time()
            qi.compress()
            print(" compress  : "+str(time() - t))
            t = time()
            qi.write_file("bbb")
            print(" file      : "+str(time() - t))
            cmp = getsize("bbb")
            print(" compressed: "+str(cmp)+" bytes")

            remove("aaa")

            print(" qi/raw    : "+str(qf/raw))
            print(" cmp/raw   : "+str(cmp/raw))
            print(" cmp/png   : "+str(cmp/png))

            q2 = quad_image()
            t = time()
            q2.read_file("bbb")
            print(" read      : "+str(time() - t))
            remove("bbb")
            t = time()
            q2.decompress()
            print(" dcmp      : "+str(time() - t))
            nd2 = q2.get_channels()
            pi = Image.fromarray(nd2)
            print(str(th)+"-"+f)
            pi.save(str(th)+"-"+f)

def test_one():
    fname = "test-images/test"
    ext = "png"
    img = Image.open(fname + "." + ext)
    npdata = asarray(img)
    png = getsize(fname + "." + ext)
    print(" dimensions: "+str(npdata.shape))
    print(" PNG       : "+str(png)+" bytes")
    dims = npdata.shape
    raw = dims[0] * dims[1] * dims[2]
    print(" raw       : "+str(raw)+" bytes")
    t = time()
    qi = quad_image(npdata)
    print(" construct : "+str(time() - t))
    t = time()
    qi.write_file(fname + "." + ext + ".qi")
    print(" file      : "+str(time() - t))
    qf = getsize(fname + "." + ext + ".qi")
    print(" quad-image: "+str(qf)+" bytes")

    t = time()
    qi.compress()
    print(" compress  : "+str(time() - t))
    t = time()
    qi.write_file(fname + "-c." + ext + ".qi")
    print(" file      : "+str(time() - t))
    cmp = getsize(fname + "-c." + ext + ".qi")
    print(" compressed: "+str(cmp)+" bytes")
    
    q2 = quad_image()
    q2.read_file(fname + "-c." + ext + ".qi")
    q2.decompress()
    nd2 = q2.get_channels()
    pi = Image.fromarray(nd2)
    pi.save(fname + "-s." + ext)

if __name__=="__main__":
    test_many()