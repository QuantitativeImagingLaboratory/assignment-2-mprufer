import numpy as np
from collections import defaultdict
import cv2 as cv

markers = [
    cv.MARKER_STAR
]

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
        stats_dict = defaultdict(list)
        wh = 0
        sumx = [0]*1000
        sumy = [0]*1000
        areas = [0]*1000
        count = 0
        counter = 0

        for i in range(w):
            for j in range(h):
                num = int(region[i,j])
                if int(region[i,j]) > 0:
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
            if len(areas_dict[areas[i]]) > 14:
                print("Region:", counter+1,", Area: ", end="")
                counter+=1
                stats_dict[wh].append(len(areas_dict[areas[i]]))
                print(str(stats_dict[wh])[1:-1], end="")
                wh+=1
                print(", Centroid: (",end="")
                stats_dict[wh].append(int(sumx[areas[i]]/len(areas_dict[areas[i]])))
                print(str(stats_dict[wh])[1:-1],end="")
                wh+=1
                stats_dict[wh].append(int(sumy[areas[i]]/len(areas_dict[areas[i]])))
                print(",", str(stats_dict[wh])[1:-1],")")
                wh+=1

        return stats_dict

    def mark_regions_image(self, image, stats):
        """Creates a new image with computed stats
        takes as input
        image: a list of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""
        (w,h) = image.shape
        count = len(stats)/3
        count = int(count)
        sg = 0
        fontsize = h/1000
        for i in range(count):
            area = int(str(stats[sg])[1:-1])
            sg+=1
            pos1 = int(str(stats[sg])[1:-1])
            sg+=1
            pos2= int(str(stats[sg])[1:-1])
            sg+=1
            region = str(i+1)
            area = str(area)
            cv.drawMarker(image, (pos2, pos1),(206,206,182),markerType=cv.MARKER_STAR,markerSize=5,thickness=1,line_type=cv.LINE_AA)
            cv.putText(image, region+","+area, (pos2+1, pos1), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, fontsize, (182,206,206))
        return image

