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
        for i in range(c):
            for j in range(b):
                outputImage[i,j] = image[int(i/scalex), int(j/scaley)]

        image = outputImage

        return image

    def bilinear_interpolation(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the bilinear interpolation method
        """

        (w,h) = image.shape
        w = w-1
        h = h-1
        scalex = float(fx)
        scaley = float(fy)
        (c, b) = (int(scalex * w), int(h * scaley))
        outputImage = np.zeros([c, b], dtype=np.uint8)

        for i in range(c):
            for j in range(b):
                if i-1 < 0:
                    x1 = i
                else:
                    x1 = i-1
                if i+1 > c:
                    x2 = i
                else:
                    x2 = i+1
                if j-1 < 0:
                    y1 = j
                else:
                    y1 = j-1
                if j+1 > b:
                    y2 = j
                else:
                    y2 = j+1

                f1 = (((x2-i)/(x2-x1))*image[int(x1/scalex),int(y1/scaley)])+(((i-x1)/(x2-x1))*image[int(x2/scalex),int(y1/scaley)])
                f2 = (((x2-i)/(x2-x1))*image[int(x1/scalex),int(y2/scaley)])+(((i-x1)/(x2-x1))*image[int(x2/scalex),int(y2/scaley)])

                f3 = (((y2-j)/(y2-y1))*f1)+(((j-y1)/(y2-y1))*f2)

                outputImage[i,j] = int(f3)

        image = outputImage

        return image
