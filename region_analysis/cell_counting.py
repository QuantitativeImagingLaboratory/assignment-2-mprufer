import numpy as np
from collections import defaultdict
import cv2 as cv
#define markers
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
        k = 1 #region counter

        for i in range(w):
            for j in range(h):
                #if index out of image range, define as 0
                if j-1 < 0:
                    image[i,j-1] = 0
                if i-1 < 0:
                    image[i-1,j] = 0
                #perform blob coloring
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
                        #iterate through image (up until current index)
                        #for every pixel with previous region number, change to new region number
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
        #make a list for each region consiting of the indices belonging to it
        #keep a sum of the x and y-coordinates to help calculate the cetroid
        for i in range(w):
            for j in range(h):
                num = int(region[i,j])
                if int(region[i,j]) > 0:
                    #encounters new region that hasn't been logged yet
                    if not areas_dict:
                        areas_dict[num].append((i,j))
                        sumx[num] += i
                        sumy[num] += j
                    #logs index into its region's list
                    else:
                        areas_dict[num].append((i,j))
                        sumx[num] += i
                        sumy[num] += j
                    #counting the number of pixels in each region to get the area
                    if num not in areas:
                        areas[count] = num
                        count+=1
        for i in range(count+1):
            if len(areas_dict[areas[i]]) > 14:
                print("Region:", counter+1,", Area: ", end="")
                counter+=1 #to ensure printing of correct region number
                stats_dict[wh].append(len(areas_dict[areas[i]])) #append to stats to be passed on to mark_regions_image
                print(str(stats_dict[wh])[1:-1], end="")
                wh+=1 #increment stats to append statistic specific to this region
                print(", Centroid: (",end="")
                stats_dict[wh].append(int(sumx[areas[i]]/len(areas_dict[areas[i]])))
                print(str(stats_dict[wh])[1:-1],end="")
                wh+=1
                stats_dict[wh].append(int(sumy[areas[i]]/len(areas_dict[areas[i]])))
                print(",", str(stats_dict[wh])[1:-1],")")
                wh+=1 #append one last time to move on to next region's statistic

        return stats_dict

    def mark_regions_image(self, image, stats):
        """Creates a new image with computed stats
        takes as input
        image: a list of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""
        (w,h) = image.shape
        count = len(stats)/3 #each region has 3 stats; must divide by 3 to get total number of regions
        count = int(count)
        sg = 0 #iterator to properly get each ergion's statistic
        fontsize = h/1000 #define font size according to image size
        #increment by region number (not by actual number of indices in stats)
        for i in range(count):
            area = int(str(stats[sg])[1:-1])
            sg+=1 #increment stats to get the next statistic in this region
            pos1 = int(str(stats[sg])[1:-1]) #get the x-coordinate of the centroid
            sg+=1
            pos2= int(str(stats[sg])[1:-1]) #get the y-coordinate of the centroid
            sg+=1
            region = str(i+1)
            area = str(area)
            cv.drawMarker(image, (pos2, pos1),(206,206,182),markerType=cv.MARKER_STAR,markerSize=5,thickness=1,line_type=cv.LINE_AA)
            cv.putText(image, region+","+area, (pos2+1, pos1), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, fontsize, (182,206,206))
        return image

