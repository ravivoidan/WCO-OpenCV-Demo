import numpy as np 
import cv2
import mediapipe as mp 
import serial   

#cap = cv2.VideoCapture(0)
cap  = cv2.VideoCapture(r"C:\Users\Idan Ravivo\Desktop\WCO OpenCV WS\handMoving.mp4")


mp_hands = mp.solutions.hands #access handtracking lib
hand = mp_hands.Hands() #calls hand tracking detector
mp_drawing = mp.solutions.drawing_utils #drawing lib to draw hand skeleton

#serialCom = serial.Serial('COM#', 9600)


while True:
    ret, frame = cap.read()
    if ret is False:
        break

    frame = cv2.resize(frame, (960, 540))
    RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #must take rgb input for mediapipe
    result = hand.process(RGBframe) 

    if result.multi_hand_landmarks: #checks for hand and maps landmarks
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            hand1 = result.multi_hand_landmarks[0]
            wristX = hand1.landmark[0].x #find x coordinate of the wrist

            motorSpeed = wristX * 255 #calculates motor speed
            #serialCom.write(bytes[motorSpeed]) #change to bytes to send to arduino





    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord('q'):
            break
    
cap.release()
cv2.destroyAllWindows()
    
