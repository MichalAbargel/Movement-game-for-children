from hands_dedector import HandDetector
import cv2


def numbers(finger, image):
    # Flip the image(frame)
    image = cv2.flip(image, 1)

    # Convert BGR image to RGB image
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    handDetector = HandDetector(min_detection_confidence=0.6)

    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    count = 0
    flag = False
    if len(handLandmarks) != 0:
        #  get y coordinate of finger-tip and check if it lies above middle landmark of that finger
        #  details: https://google.github.io/mediapipe/solutions/hands
        if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:  # Right Thumb
            count = count + 1
        elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:  # Left Thumb
            count = count + 1
        if handLandmarks[8][2] < handLandmarks[6][2]:  # Index finger
            count = count + 1
        if handLandmarks[12][2] < handLandmarks[10][2]:  # Middle finger
            count = count + 1
        if handLandmarks[16][2] < handLandmarks[14][2]:  # Ring finger
            count = count + 1
        if handLandmarks[20][2] < handLandmarks[18][2]:  # Little finger
            count = count + 1
    if count != int(finger):
        flag = False
        return image, flag
        # cv2.putText(image, "you need to show number: " + str(finger), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 12, cv2.LINE_AA)
    else:
        flag = True
        # cv2.putText(image, str(count), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 25)
        return image, flag