import numpy as np 
import cv2
import mediapipe as mp 
import serial 
import time


# Connect to Arduino before the loop
serialCom = serial.Serial("COM3", 9600, timeout=1)
time.sleep(2)  # Allow Arduino to reset

cap = cv2.VideoCapture(0)


mp_hands = mp.solutions.hands #access handtracking lib
hand = mp_hands.Hands() #calls hand tracking detector
mp_drawing = mp.solutions.drawing_utils #drawing lib to draw hand skeleton

#serialCom = serial.Serial('COM#', 9600)


lastServoDegree = None

try:
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


                servoDegree = int(wristX * 180) #calculates degree

                # Limit angle to 0-180
                servoDegree = max(0, min(180, servoDegree))

                # Send only when the angle changes
                if servoDegree != lastServoDegree:
                    serialCom.write(f"{servoDegree}\n".encode())
                    lastServoDegree = servoDegree

                    print("Sent:", servoDegree)



        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord('q'):
                break
finally:  
    cap.release()
    cv2.destroyAllWindows()
    serialCom.close()
