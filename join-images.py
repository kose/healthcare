#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2 as cv

def main():

    image_proc = cv.imread("images/blood-pressure.png")

    for filename in ["images/body-mass.png", "images/body-temperature.png", "images/distance-walking.png"]:
    
        image = cv.imread(filename)
    
        image_proc = cv.vconcat([image_proc, image])

    cv.imwrite("images/helthcare.png", image_proc)
    print("create images/helthcare.png")
    
    # cv.imshow("image", image_proc)
    # cv.waitKey(0)
    
    
if __name__ == '__main__':
    main()

# import pdb; pdb.set_trace()

### Local Variables: ###
### truncate-lines:t ###
### End: ###
