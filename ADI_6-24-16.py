import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob
from astropy.io import fits
from skimage.transform import rotate as skirotate

#Take 2d image (numpy array of intensity values) as input and returns
#a 1d array of azimuthal radial average values indexed by radius (in pixels)
def radial_profile(image):
    xcent = image.shape[1]/2.0
    ycent = image.shape[0]/2.0
    y, x = np.indices((image.shape))
    r = abs((x-xcent)+1j*(y-ycent))
    r = r.astype(np.int)
    tbin = np.bincount(r.ravel(), image.ravel())
    nr = np.bincount(r.ravel())
    radialprofile = tbin / nr
    return radialprofile

#Take the radial_profile(image) 1d array r and create an image with the same
#dimensions as image with pixels (x,y) such that r = sqrt(x**2 + y**2)
def build_radial_image(image):
    xcent = image.shape[1]/2.0
    ycent = image.shape[0]/2.0
    radImage = np.zeros(image.shape)
    radialData = radial_profile(image)
    for index, value in np.ndenumerate(radImage):
        y, x = index
        r = int(abs((x-xcent)+1j*(y-ycent)))
        radImage[index] = radialData[r]
    return radImage

#Take an original image and return the original image centered in a larger
#image with border value=0 and x,y dimensions = diagonal length of the
#original image
def fitImageToRotation(image):
    yHeight, xWidth = image.shape
    diagonalLength = int(abs(xWidth+1j*yHeight))
    largerImage = np.zeros((diagonalLength, diagonalLength))
    xStart = (diagonalLength - xWidth)/2
    yStart = (diagonalLength - yHeight)/2
    for index, value in np.ndenumerate(image):
        y, x = index
        largerImage[((y + yStart) , (x + xStart))] = image[index]   
    return largerImage

#Take an image and sets the np.amin(image) to 0 and the max to 10000
def normalizeImageIntensity(image):
    normalizedImage = np.zeros(image.shape)
    minIntensity = np.amin(image)
    deltaIntensity = float(np.amax(image) - minIntensity)/10000.0
    normalizedImage = np.divide( (image - minIntensity) , deltaIntensity)
    #normalizedImage = image - minIntensity
    return normalizedImage

#Takes an image and rotates it counterclockwise by the given parallactic angle
def rotateImage(image, angle):
    return skirotate(image, angle, preserve_range = True)

#Create a list of image files to open in the fold given by path
path = "C://Users//Augustine//Documents//Angular-Differential-Imaging//cxsxbcponlm//DX_1//"
image_list = sorted(glob(os.path.join(path, '*.fits')))

#Create a list of parallactic angles for the images in the image_list
angleList = []
fin = open(path + 'DX_1_parallactic_angles.txt', 'r')
angleList = list(map(float, fin.read().split()))
fin.close()

#Create a 3d stack of 2d image arrays
image_stack = [ fits.getdata(image) for image in image_list ]
#The long way
#image_stack = []
#for image in image_list:
#    image_stack.append(fits.getdata(image))

#Calculate the median along the vertical axis of this 3d stack of 2d arrays
#axis = 0 is refers to the vertical (stacking) axis of the 2d images
image_median = np.median(image_stack, axis = 0) 

#Subtract the median image from the image_stack
image_stack_large = []
j=0
for image in image_stack:
    medianSubtracted = np.subtract(image, image_median)
    radialSubtracted = np.subtract(medianSubtracted, build_radial_image(medianSubtracted))
    largeImage = fitImageToRotation(radialSubtracted)
    #Flip the inverted image because the array (0,0) -upper left- is the lower left of the image
    image_stack_large.append(skirotate(largeImage, -(angleList[0]-angleList[j])))
    j += 1

#Plot the resulting angular differential image
plt.figure(1)
plt.imshow(np.median(image_stack_large, axis = 0), cmap='gray', origin='lower')
plt.colorbar()
plt.show()
