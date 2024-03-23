import cv2
import numpy as np

global HSV

def Life2CodingRGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  # checks mouse moves
        colorsHSV = HSV[y, x]
        print("HSV Value at ({},{}):{} ".format(x,y,colorsHSV))

# using camera 0
cap = cv2.VideoCapture(3)

while cap.isOpened():
    ret,frame = cap.read()
    # 1- convert frame from BGR to HSV
    HSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
# Create a window and set Mousecallback to a function for that window
    cv2.namedWindow('Tracking Green Color')
    cv2.setMouseCallback('Tracking Green Color', Life2CodingRGB)
    # 2- define the range of green
    lower=np.array([50, 180, 50])
    upper=np.array([70, 255, 255])

    #check if the HSV of the frame is lower or upper red
    Green_mask = cv2.inRange(HSV,lower, upper)
    result = cv2.bitwise_and(frame, frame, mask = Green_mask)

    # Draw rectangular bounded line on the detected red area
    (contours, hierarchy) = cv2.findContours(Green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300): #to remove the noise
            # Constructing the size of boxes to be drawn around the detected green area
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imshow("Tracking Green Color",frame)
    cv2.imshow("Mask",Green_mask)
    cv2.imshow("And",result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()