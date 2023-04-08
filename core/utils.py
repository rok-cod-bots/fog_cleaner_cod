import os
import sys
from com.dtmilano.android.viewclient import ViewClient
import cv2 
import time
import numpy as np

# Create an ADB device and connect it to Bluestacks
def connectToBluestacks():
    print('■ - Checking adb devices...')
    output_stream = os.popen('adb devices')
    outp = output_stream.read()
    outp = outp.split('\n')
    outp.remove('List of devices attached')

    while("" in outp):
        outp.remove("")

    if len(outp) > 1: 
        print("Your devices: " + str(outp))
        print('X - Please make sure you only have 1 emulator opened.')
        sys.exit()

    device, serialno = ViewClient.connectToDeviceOrExit()
    print('≡ - Connected to adb device ['+ str(serialno) + ']')

    time.sleep(1)

    return device

# Find the position of one pattern from an image
def findPattern(image, pattern, debug=False):
    large_image = cv2.imread(image)
    small_image = cv2.imread(pattern)

    # Find the width and height of the smaller image
    h, w = small_image.shape[:2]

    # Match the smaller image to the larger image
    result = cv2.matchTemplate(small_image, large_image, cv2.TM_CCOEFF_NORMED)

    # Get the coordinates of the best match 
    _, _, _, top_left = cv2.minMaxLoc(result)

    # Debug with a rectangle box
    if debug == True :
        cv2.rectangle(large_image, top_left, (top_left[0] + w, top_left[1] + h), (0, 0, 255), 2)
        cv2.imshow('result', large_image)
        cv2.waitKey()
        cv2.destroyAllWindows()
        return 0, 0
   
    
    return top_left[0] + w / 2, top_left[1] + h / 2

# Find the positions of multiples patterns from an image
def findMultiplePatterns(image, pattern, debug=False):  
    # Load the image and the pattern
    large_image = cv2.imread(image)
    small_image = cv2.imread(pattern)

    # Find the positions of the pattern in the image using cv2.matchTemplate()
    result = cv2.matchTemplate(large_image, small_image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    locations = np.where(result >= threshold)

    # Extract the coordinates and size of the bounding boxes for each occurrence of the pattern
    h, w = small_image.shape[:-1]
    rectangles = []
    for pt in zip(*locations[::-1]):
        rectangles.append([pt[0], pt[1], w, h])

    # Apply non-maximum suppression to the bounding boxes
    rectangles = np.array(rectangles)
    confidences = np.ones(len(rectangles))
    nms_rectangles = cv2.dnn.NMSBoxes(rectangles, confidences, 0.5, 0.4)

    positions = []
    # Get the positions of the patterns found
    for i in nms_rectangles:
        x, y, w, h = rectangles[i]
        positions.append([x + w / 2, y + h / 2])
        cv2.rectangle(large_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    if debug == True:
        cv2.imshow('Matches', large_image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    return positions

# Use ADB to click on the selected pixel with 1 second of sleep after the click
def click(device, position):
    device.shell('input tap ' + str(position[0]) + ' ' + str(position[1]))
    time.sleep(1.5)

# Take a screenshot from the Bluestacks app and return the path's screen
def takeScreenshot():
    path = "images/screen.png"
    os.popen('adb exec-out screencap -p > ' + path)

    time.sleep(2)

    return path