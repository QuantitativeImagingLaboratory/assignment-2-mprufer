import cv2, numpy as np, matplotlib.pyplot as mat, math
from decimal import Decimal

class resample:
    def resize(self, image, fx=None, fy=None, interpolation=None):
        """calls the appropriate funciton to resample an image based on the interpolation method
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        interpolation: method used for interpolation ('either bilinear or nearest_neighbor)
        returns a resized image based on the interpolation method
        """

        if interpolation == 'bilinear':
            return self.bilinear_interpolation(image, fx, fy)

        elif interpolation == 'nearest_neighbor':
            return self.nearest_neighbor(image, fx, fy)

    def nearest_neighbor(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the nearest neighbor interpolation method
        """
        #getting dimensions + calculating resampled size
        (w,h) = image.shape
        scalex = float(fx)
        scaley = float(fy)
        (c,b) = (int(scalex*w), int(h*scaley))
        outputImage = np.zeros([c,b],dtype=np.uint8)

        #calculate intensities for new image
        for i in range(c-1):
            for j in range(b-1):
                tempx = int(round(i/float(fx)))
                tempy = int(round(j/float(fy)))

                #prevent access to out-of-bound indexes
                if (tempx >= w):
                    tempx = tempx-1
                if (tempy == h):
                    tempy = tempy-1

                #prevent assigning values that are out-of-bounds
                if (tempx+1) >= w:
                    (n1x,n1y) = (tempx,tempy)
                else:
                    (n1x,n1y) = (tempx+1, tempy)
                if (tempx-1) < 0:
                    (n2x, n2y) = (tempx, tempy)
                else:
                    (n2x, n2y) = (tempx-1, tempy)
                if (tempy+1) >= h:
                    (n3x,n3y) = (tempx, tempy)
                else:
                    (n3x,n3y) = (tempx,tempy+1)
                if (tempy-1) < 0:
                    (n4x,n4y) = (tempx,tempy)
                else:
                    (n4x,n4y) = (tempx,tempy-1)

                #calculate distances of each neighbor
                dist1 = (math.sqrt(((n1x-i)**2)+((n1y-j)**2)))
                dist2 = (math.sqrt(((n2x-i)**2)+((n2y-j)**2)))
                dist3 = (math.sqrt(((n3x-i)**2)+((n3y-j)**2)))
                dist4 = (math.sqrt(((n4x-i)**2)+((n4y-j)**2)))

                #find nearest neighbor & assign its intensity to new image
                nearest = dist1
                outputImage[i,j] = image[n1x,n1y]
                if (dist2 < nearest):
                    outputImage[i,j] = image[n2x,n2y]
                if(dist3 < nearest):
                    outputImage[i,j] = image[n3x,n3y]
                if(dist4 < nearest):
                    outputImage[i,j] = image[n4x,n4y]

        image = outputImage

        return image

    def bilinear_interpolation(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the bilinear interpolation method
        """

        # Write your code for bilinear interpolation here

        return image
