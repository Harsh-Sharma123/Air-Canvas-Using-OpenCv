import cv2
import numpy as np
from collections import deque

# default trackbar function
def hello(x):
    print("")

# creating trackbars needed for adjusting the marker color
cv2.namedWindow("Color Detector")

cv2.createTrackbar("Upper Hue", "Color Detector", 153, 180, hello)
cv2.createTrackbar("Upper Saturation", "Color Detector", 255, 255, hello)
cv2.createTrackbar("Upper Value", "Color Detector", 255, 255, hello)
cv2.createTrackbar("Lower Hue", "Color Detector", 64, 180, hello)
cv2.createTrackbar("Lower Saturation", "Color Detector", 72, 255, hello)
cv2.createTrackbar("Lower Value", "Color Detector", 49, 255, hello)

# Creating different arrays to handle different colour points
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# These indexes will be used to mark the points in a particular array of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# Kernel to be used for dilation purpose
kernel = np.ones((5,5), np.uint8)

colors = [(255,0,0), (0,255,0), (0,0,255), (0,255,255)]
colorIndex = 0

# Here is code for Canvas setup
paintWindow = np.zeros((471,636,3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

cv2.putText(paintWindow, "CLEAR", (49,33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185,33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298,33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420,33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

cv2.namedWindow("Paint", cv2.WINDOW_AUTOSIZE)

# Opening default webcam of pc
cap = cv2.VideoCapture(0)

# Keep Recording
while(True):
    # Reading the frame from the camera
    ret, frame = cap.read()

    # Flipping the frame to see same side of yours
    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # u_hue = cv2.getTrackbarPos("Upper Hue", "Color Detector")
    # u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color Detector")
    # u_value = cv2.getTrackbarPos("Upper Value", "Color Detector")
    # l_hue = cv2.getTrackbarPos("Lower Hue", "Color Detector")
    # l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color Detector")
    # l_value = cv2.getTrackbarPos("Lower Value", "Color Detector")

    u_hue = cv2.getTrackbarPos("Upper Hue", "Color Detector")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color Detector")
    u_value = cv2.getTrackbarPos("Upper Value", "Color Detector")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color Detector")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color Detector")
    l_value = cv2.getTrackbarPos("Lower Value", "Color Detector")

    upper_hsv = np.array([u_hue, u_saturation, u_value])
    lower_hsv = np.array([l_hue, l_saturation, l_value])

    # adding the color buttons to live frame for colour access
    frame = cv2.rectangle(frame, (40,1), (140, 65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,1), (255, 65), colors[0], -1)
    frame = cv2.rectangle(frame, (275,1), (370, 65), colors[1], -1)
    frame = cv2.rectangle(frame, (390,1), (485, 65), colors[2], -1)
    frame = cv2.rectangle(frame, (505,1), (600, 65), colors[3], -1)

    cv2.putText(frame, "CLEAR ALL", (49,33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185,33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298,33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420,33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520,33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

    # Identifying the pointer by making its mask
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # find contours fo the pointer after identifying it
    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # if the contours are formed
    if len(cnts)>0:
        # sorting the contour to find the biggest
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        # get the radius of the enclosing circle around the contour
        ((x,y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (10,255,255,), 2)
        # Calculating the center of the detected contour
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        # Now checking if the user wants to click pn any button above the screen
        if center[1] <= 65:
            if 40 <= center[0] <= 140:   # clear button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0

                paintWindow[67:,:,:] = 255
            elif 160 <= center[0] <=255:
                colorIndex = 0      # Blue
            elif 275 <= center[0] <= 370:
                colorIndex = 1  #Green
            elif 390 <= center[0] <= 485:
                colorIndex = 2  #Red
            elif 505 <= center[0] <= 600:
                colorIndex = 3  #Yellow
            
        else:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)

    # Append the next deque when nothing is detected to avoid messing up
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # Draw the lines of all the colors on the canvas and frame
    points = [bpoints, gpoints,  rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k-1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k-1], points[i][j][k], colors[i], 2)
    
    # Show all the windows
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("Mask", mask)

    # If the user presses q key then quit:
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and all the resources
cap.release()
cv2.destroyAllWindows()