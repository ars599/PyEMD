"""
EEMD & EMD
Org EEMD Author: Dawid Laszuk

Matalb EEMD2D
Org: from https://github.com/leeneil
convert from leeneil to python
owned by Arnold Sullivan
history 08 10 2017
Oceans and Atmosphere CSIRO
web: arnold.sullivan@csiro.au
"""
from __future__ import division, print_function

import numpy  as np
import pylab as plt
from eemd2d import eemd2d

# Generate image
print("Generating image... ", end="")
rows, cols = 256, 256
row_scale, col_scale = 256, 256
x = np.arange(rows)/float(row_scale)
y = np.arange(cols).reshape((-1,1))/float(col_scale)

pi2 = 2*np.pi
img = np.zeros((rows,cols))
img = img + np.sin(2*pi2*x)*np.cos(y*4*pi2+4*x*pi2)
#img = img + np.cos(7*pi2*y)
#*np.cos(y*4*pi2+4*x*pi2)
#img = img + 3*np.sin(2*pi2*x)+2
#img = img + 5*x*y + 2*(y-0.2)*y
print("Done")

# Perform decomposition
print("Performing decomposition... ", end="")
#emd2d = EMD2D()
#emd2d.FIXE_H = 5
#IMFs = emd2d.emd(img, max_imf=4)
data = eemd2d(img,8,0.001)
IMFs = data[2]
imfNo = IMFs.shape[2]
print("Done")

print("Saving array... ")
import pickle
output = open('data_imfs.pkl', 'wb')
pickle.dump(data, output)
output.close()

print("Plotting results... ", end="")

# Save image for preview
#plt.figure(figsize=(4,4*(imfNo+1)))
#plt.subplot(imfNo+1, 1, 1)
plt.imshow(img)
plt.colorbar()
plt.title("Input image")
plt.savefig("image_signal4.eps")

# Save reconstruction
#for n, imf in enumerate(IMFs):
#for n in range(0, imfNo):
for n in range(0, imfNo):
    plt.subplot(imfNo/2., 2, n+1)
    plt.imshow(IMFs[:,:,n])
    plt.colorbar()
    plt.title("IMF %i"%(n+1))

plt.savefig("image_decomp_eemd_arnold1.eps")
print("Done")

