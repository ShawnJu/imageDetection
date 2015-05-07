from PIL import Image
import numpy as np

if __name__ == "__main__":
    dir = "./xinkeliu_temp/"
    im = Image.open(dir + "xinkeliu 1.png")
    temp =  np.asarray(list(im.getdata()))

    print temp.shape

