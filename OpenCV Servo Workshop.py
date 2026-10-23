import numpy as np 
import cv2

#cap = cv2.VideoCapture(0)
cap  = cv2.VideoCapture(r"C:\Users\Idan Ravivo\Desktop\WCO OpenCV WS\traffic.mp4")
#width = int(cap.get(3)) #1920
#height = int(cap.get(4)) #1080   

handDetector = cv2.createBackgroundSubtractorMOG2() #figures out background through what is stationary and what isnt

while True:
    ret, frame = cap.read()
    if ret is False:
        break

    frame = cv2.resize(frame, (960, 540)) #only necessary for video testing remove once doing hand testing
    mask = handDetector.apply(frame) #creates a mask so turns hand white and background black based on the background subtractor

    contours, heirarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #simple only tracks the four corners and external only tracks the perimiter
    maxContour = max(contours, key = cv2.contourArea) #finds the largest area contour/white space. returns the top left corner point
    x,y,w,h = cv2.boundingRect(maxContour) # returns data needed to creat a rectangle around largest contour

    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2) 
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

