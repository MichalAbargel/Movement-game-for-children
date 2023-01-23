import math
import random
import time
import PIL
import numpy as np
import cv2
from tkinter import *
from PIL import ImageTk, Image
from cvzone.HandTrackingModule import HandDetector
import cvzone
from music_player import play_click
# webcome
# cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1699990)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1299990)
# cap.set(3, 1280)
# cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


def analyze_points_frame(image,counter, score,cx, cy,time_start,game_over):
    # Find Function
    x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
    y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    coff = np.polyfit(x, y, 2)

    color = (170, 213, 34)
    total_time = 10

    # Flip the image(frame)
    img = cv2.flip(image, 1)

    hands = detector.findHands(img, draw=False)
    if time.time() - time_start < total_time:
        if hands:
            lmList = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']
            x1 = lmList[5][0]
            y1 = lmList[5][1]
            # x1, y1 = lmList[5]
            x2 = lmList[17][0]
            y2 = lmList[17][1]
            # x2, y2 = lmList[17]
            distance = int(math.sqrt((y2-y1) ** 2 + (x2-x1) ** 2))
            A, B, C = coff
            distance_CM = A*distance**2 + B*distance + C
            if distance_CM < 80:
                if x < cx < x+w and y < cy < y+h:
                    counter = counter + 1
                    color = (224, 22, 233)
                    play_click()
            cv2.rectangle(img,(x, y), (x+w, y+h), (201, 174, 104), 3)
            cvzone.putTextRect(img, f'{int(distance_CM)} cm', (x+5, y-10),  colorR=(201, 174, 104))
            if counter == 10:
                # 590 350
                cx = random.randint(10, 590)
                cy = random.randint(10, 350)
                color = (201, 174, 104)
                score += 1
                counter = 0

        # Draw Button
        cv2.circle(img,(cx, cy),30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (225, 225, 225), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (225, 225, 225), 2)
        cv2.circle(img, (cx, cy), 30, (50,50, 50), 2)
        # Game HUD
        cvzone.putTextRect(img, f'Time: {int(total_time-(time.time()-time_start))}', (60, 120),scale=2, colorR=(201, 174, 104), offset=10)
        cvzone.putTextRect(img, f'Score: {str(score).zfill(2)}', (60, 75), scale=2, colorR=(201, 174, 104), offset=10)
    else:
        game_over = True
        cvzone.putTextRect(img, 'GAME OVER', (50, 140), colorT=(104, 174, 201), scale=5, offset=8, thickness=7)
        cvzone.putTextRect(img, f'Your Score: {score}', (70, 200), colorT=(104, 174, 201), scale=3, offset=2, thickness=5)
    return img, game_over, score, counter