# -*- coding: utf-8 -*-
"""
Simple example allows for a selected region to be zoomed.  The selected region is resized and
joined horizontally to the main image

@author: Roger Woodman
"""
import cv2
import numpy

class ZoomRegion():

    def __init__(self, image):    
        """Initialise drawing variables"""
        # Flag for wether the user has clicked and now dragging
        self.drawing = False
        # Points for the rectangle
        self.point1 = (-1, -1)
        self.point2 = (-1, -1)
        # Initial image
        self.imageMain = image
        # Image to draw on
        self.imageDraw = self.imageMain.copy()    

    def draw(self, event, x, y, params, flags):
        """Handles mouse callback events"""
        if(event == cv2.EVENT_LBUTTONDOWN and not self.drawing):
            self.drawing = True
            self.point1 = (x, y)
        if (event == cv2.EVENT_MOUSEMOVE and self.drawing):
            self.imageDraw = self.imageMain.copy()
            self.point2 = (x, y)
            cv2.rectangle(self.imageDraw, self.point1, self.point2, (0,255,0), 1)
            
            # Flip the points if the rectangle has been created from bottom to top or right to left
            roiPoint1 = list(self.point1)
            roiPoint2 = list(self.point2)
            if(roiPoint1[0] > roiPoint2[0]):
                roiPoint1[0], roiPoint2[0] = roiPoint2[0], roiPoint1[0]
            if(roiPoint1[1] > roiPoint2[1]):
                roiPoint1[1], roiPoint2[1] = roiPoint2[1], roiPoint1[1]
            # Get the region of interest
            imageROI = self.imageMain[roiPoint1[1]:roiPoint2[1], roiPoint1[0]:roiPoint2[0]]
            
            # If the region is larger than 1 x 1 then reszize the selected region
            if(imageROI.shape[0] > 1 and imageROI.shape[1] > 1):
                imageROI = cv2.resize(imageROI, (0,0), fx=3, fy=3) 
            
            # Get image and ROI dimensions
            height1, width1 = self.imageDraw.shape[:2]
            height2, width2 = imageROI.shape[:2]
            # Create empty matrix
            tempImage = numpy.zeros((max(height1, height2), width1+width2,3), numpy.uint8)
            # Combine 2 images
            tempImage[:height1, :width1,:3] = self.imageDraw
            tempImage[:height2, width1:width1+width2,:3] = imageROI
            # Set image to draw as combination of two images
            self.imageDraw = tempImage
        if event == cv2.EVENT_LBUTTONUP:
            if(self.drawing):
                self.point2 = x, y
            self.drawing = False

if __name__ == '__main__':

    # Load image
    #image = numpy.zeros((512, 512, 3), numpy.uint8)
    image = cv2.imread(r'test_image.jpg')
    # Create drawing object
    drawTest = ZoomRegion(image)
    # Create an openCV window
    cv2.namedWindow('Simple image zoom')
    # Attach an even handler to the window
    cv2.setMouseCallback('Simple image zoom', drawTest.draw)
    print("Press Escape to exit the program")
    
    # Loop until user presses escape
    while(True):
        cv2.imshow('Simple image zoom', drawTest.imageDraw)
        # Press escape to exit the program
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        
    # close CV window
    cv2.destroyAllWindows()