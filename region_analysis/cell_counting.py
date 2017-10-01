import numpy as np
from collections import defaultdict

class cell_counting:

    def blob_coloring(self, image):
        """Uses the blob coloring algorithm based on 8 pixel window assign region names
        takes a input:
        image: binary image
        return: a list of regions"""

        (w,h) = image.shape

        regions = np.zeros([w, h])

        k = 1
        for i in range(w):
            for j in range(h):
                if j-1 < 0:
                    image[i,j-1] = 0
                if i-1 < 0:
                    image[i-1,j] = 0
                if image[i,j]>0 and image[i,j-1]==0 and image[i-1,j]==0:
                    regions[i,j]=int(k)
                    k=k+1
                elif image[i,j]>0 and image[i-1,j]>0 and image[i,j-1]==0:
                    regions[i,j] = regions[i-1,j]
                elif image[i,j]>0 and image[i,j-1]>0 and image[i-1,j]==0:
                    regions[i,j] = regions[i,j-1]
                elif image[i,j]>0 and image[i-1,j]>0 and image[i,j-1]>0:
                    regions[i,j] = regions[i-1,j]
                    if regions[i,j-1]!=regions[i-1,j]:
                        c=0
                        b=0
                        for c in range(w):
                            for b in range(h):
                                if regions[c,b]==regions[i,j-1]:
                                    regions[c,b] = regions[i-1,j]

        return regions

    def compute_statistics(self, region):
        """Compute cell statistics area and location
        takes as input
        region: a list of pixels in a region
        returns: area"""

        (w,h) = region.shape
        areas_dict = defaultdict(list)
        num = 0
        sumx = [0]*1000
        sumy = [0]*1000
        areas = [0]*1000
        count = 0
        stats = ['']*1000

        for i in range(w):
            for j in range(h):
                num = int(region[i,j])
                if not areas_dict:
                    areas_dict[num].append((i,j))
                    sumx[num] += i
                    sumy[num] += j
                else:
                    areas_dict[num].append((i,j))
                    sumx[num] += i
                    sumy[num] += j
                if num not in areas:
                    areas[count] = num
                    count+=1
        for i in range(count+1):
            print("Region", ":",i,"Area:", len(areas_dict[areas[i]]), "Centroid:", "(", int(sumx[areas[i]]/len(areas_dict[areas[i]])),int(sumy[areas[i]]/len(areas_dict[areas[i]])),")")

        # Please print your region statistics to stdout
        # <region number>: <location or center>, <area>
        # print(stats)

        return 0

    def mark_regions_image(self, image, stats):
        """Creates a new image with computed stats
        takes as input
        image: a list of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""
        return image

