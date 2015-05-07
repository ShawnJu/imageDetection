__author__ = 'ShangJu'

import os
import scipy
import scipy.misc
import PIL.Image as Image

import numpy as np
import numpy.linalg as lin

# total count of faces
L = 14

# list file directories
basedir = 'temp/'
flist = os.listdir(basedir)

# create zero array
arr = np.zeros((L, 512*512))

num = 0

# load data matrix out of PGM files
for f in flist:
     # construct target
     if f.startswith("."):
         continue
     tfile = basedir + str(f)
     try:
        print "Opening:", tfile
        im = Image.open(tfile)
        print(type(im))
        print "Storing image in memory matrix"
        for i in xrange(im.size[0]):
           for j in xrange(im.size[1]):
               pix = im.getpixel((i,j))
               arr[num,i+j*im.size[0]] = (pix[0] + pix[1] + pix[2])/3
        num += 1
     except:
        pass

arr = arr / 256

# subtract the mean image from each image sample
for i in xrange(arr.shape[0]):
    arr[i,:] = arr[i,:] - arr.mean(0)

# compute SVD of the data matrix
print "Computing sparse SVD of data matrix"
U, V, T = lin.svd(arr.transpose(), full_matrices=False)

# print eigenfaces to files
print "Writing eigenvectors to disk..."
for i in xrange(L):
   scipy.misc.imsave('eigenface_' + str(i) + '.png', U[:,i].reshape(512,512))