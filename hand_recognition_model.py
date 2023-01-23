from datetime import time
import time
import mediapipe as mp
import cv2
# Used to convert protobuf message to a dictionary.
from google.protobuf.json_format import MessageToDict


def deditiction_hands(image, order,time_start,game_over):
    # class takes total_time seconds
    total_time = 20
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=False,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.75,
        max_num_hands=2)
    # Flip the image(frame)
    image = cv2.flip(image, 1)
    # Convert BGR image to RGB image
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the RGB image
    results = hands.process(imgRGB)
    win = 'idle'
    # If hands are present in image(frame)
    if results.multi_hand_landmarks:
        # Both Hands are present in image(frame)
        if len(results.multi_handedness) == 2 and order == 2:
            # Display 'Both Hands' on the image
            cv2.putText(image, 'Both Hands - well done!!', (250, 50),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.9, (51, 255, 255), 2)
            print("both")
            win = 'win'
            return image, win,game_over
        # If any hand present
        elif results.multi_handedness != 2:
            if order == 2:
                win = 'lose'
                return image, win, game_over
            for i in results.multi_handedness:
                # Return whether it is Right or Left Hand
                label = MessageToDict(i)
                label = label['classification'][0]['label']
                if label == 'Left' and order == 1:
                    # Display 'Left Hand' on
                    # left side of window
                    cv2.putText(image, label + ' Hand - well done!!',
                                (20, 50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.9, (51, 255, 255), 2)
                    win = 'win'
                    return image, win, game_over
                elif label == 'Right' and order == 0:
                    # Display 'Left Hand'
                    # on left side of window
                    cv2.putText(image, label + ' Hand - well done!!', (250, 50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.9, (51, 255, 255), 2)
                    win = 'win'
                    return image, win,game_over
                win = 'lose'

    if time.time() - time_start >= total_time:
        game_over = True
    return image, win, game_over