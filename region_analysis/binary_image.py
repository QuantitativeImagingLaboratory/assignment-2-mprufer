import numpy as np

class binary_image:

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram"""

        (w,h) = image.shape
        hist = [0]*w
        for i in range(w):
            for j in range(h):
                intensity = image[i,j]
                hist[intensity] += 1

        return hist

    def find_optimal_threshold(self, hist):
        """analyses a histogram it to find the optimal threshold value assuming a bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value"""

        threshold = 0
        mode1 = hist.index(max(hist))

        if mode1 == 0:
            mode2 = hist.index(max(hist[1:]))
        elif mode1 == 255:
            mode2 = hist.index(max(hist[0:mode1]))
        else:
            tempmode = hist.index(max(hist[0:mode1]))
            tempmode2 = hist.index(max(hist[mode1:]))
            if tempmode > tempmode2:
                mode2 = tempmode
            else:
                mode2 = tempmode2

        if mode1 > mode2:
            temp = mode1
            mode1 = mode2
            mode2 = temp

        largest = hist[mode2]
        threshold = (mode1+mode2)/2
        avg1 = 0
        avg2 = 1
        end = len(hist)
        total=0

        for i in range(end):
            total += hist[i]
        for i in range(end):
            hist[i] = hist[i]/total
        while avg1 != avg2:
            ex1 = 0
            ex2 = 0
            avg1 = threshold
            for i in range(int(threshold)):
                ex1 += hist[i]*i
            for i in range(int(threshold),end):
                ex2 += hist[i]*i
            threshold = (ex1+ex2)/2
            avg2 = threshold

        return threshold

    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        take as input
        image: an grey scale image
        returns: a binary image"""
        (w, h) = image.shape
        hist = [0] * w
        for i in range(w):
            for j in range(h):
                intensity = image[i, j]
                hist[intensity] += 1

        threshold = 0
        mode1 = hist.index(max(hist))

        if mode1 == 0:
            mode2 = hist.index(max(hist[1:]))
        elif mode1 == 255:
            mode2 = hist.index(max(hist[0:mode1]))
        else:
            tempmode = hist.index(max(hist[0:mode1]))
            tempmode2 = hist.index(max(hist[mode1:]))
            if tempmode > tempmode2:
                mode2 = tempmode
            else:
                mode2 = tempmode2

        if mode1 > mode2:
            temp = mode1
            mode1 = mode2
            mode2 = temp

        largest = hist[mode2]
        threshold = (mode1 + mode2) / 2
        avg1 = 0
        avg2 = 1
        end = len(hist)
        total = 0

        for i in range(end):
            total += hist[i]
        for i in range(end):
            hist[i] = hist[i] / total
        while avg1 != avg2:
            ex1 = 0
            ex2 = 0
            avg1 = threshold
            for i in range(int(threshold)):
                ex1 += hist[i] * i
            for i in range(int(threshold), end):
                ex2 += hist[i] * i
            threshold = (ex1 + ex2) / 2
            avg2 = threshold

        for i in range(w):
            for j in range(h):
                if image[i,j] < threshold:
                    image[i,j] = 0
                if image[i,j] >= threshold:
                    image[i,j] = 255
        bin_img = image.copy()

        return bin_img


