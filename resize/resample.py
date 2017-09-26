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
                tempx = int(round((i/float(fx))))
                tempy = int(round((j/float(fy))))

                #prevent access to out-of-bound indexes
                if (tempx >= w):
                    tempx = tempx-1
                if (tempy >= h):
                    tempy = tempy-1

                #prevent assigning values that are out-of-bounds
                if (tempx+1) >= w:
                    (n1x,n1y) = (None,None)
                else:
                    (n1x,n1y) = (tempx+1, tempy)
                if (tempx-1) <= 0:
                    (n2x, n2y) = (None, None)
                else:
                    (n2x, n2y) = (tempx-1, tempy)
                if (tempy+1) >= h:
                    (n3x,n3y) = (None, None)
                else:
                    (n3x,n3y) = (tempx,tempy+1)
                if (tempy-1) <= 0:
                    (n4x,n4y) = (None,None)
                else:
                    (n4x,n4y) = (tempx,tempy-1)


                #calculate distances of each neighbor
                if n1x == None:
                    dist1 = float('inf')
                else:
                    dist1 = (np.sqrt(((i-n1x)**2)+((j-n1y)**2)))
                if n2x == None:
                    dist2 = float('inf')
                else:
                    dist2 = (np.sqrt(((i-n2x)**2)+((j-n2y)**2)))
                if n3y == None:
                    dist3 = float('inf')
                else:
                    dist3 = (np.sqrt(((i-n3x)**2)+((j-n3y)**2)))
                if n4y == None:
                    dist4 = float('inf')
                else:
                    dist4 = (np.sqrt(((i-n4x)**2)+((j-n4y)**2)))

                #find nearest neighbor & assign its intensity to new image
                nearest = dist1
                if dist1 == float('inf'):
                    outputImage[i,j] = image[n2x,n2y]
                else:
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
