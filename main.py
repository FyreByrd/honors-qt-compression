#!/usr/bin/python3
from PIL import Image
from numpy import asarray

if __name__=="__main__":
    image = Image.open("test.png")

    numpydata = asarray(image)
    
    print(type(numpydata))
    print(numpydata.shape)

    pilImage = Image.fromarray(numpydata)
    print(type(pilImage))
    
    # Let us check  image details
    print(pilImage.mode)
    print(pilImage.size)