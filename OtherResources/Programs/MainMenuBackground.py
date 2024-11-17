import os
import shutil
import cv2
import numpy as np

MainMenuBackgroundDir = '../media/videos/MainMenuBackgroundDimmed'

if os.path.exists(MainMenuBackgroundDir):
    shutil.rmtree(MainMenuBackgroundDir)

os.makedirs(MainMenuBackgroundDir)

cap = cv2.VideoCapture('../../media/videos/MainMenuBackground.mp4')

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Blur Image
    BlurIndex = 75
    blurred_frame = cv2.GaussianBlur(frame, (BlurIndex, BlurIndex), 0)

    # Reduce brightness
    brightness_factor = 0.5
    dark_frame = np.zeros(frame.shape, frame.dtype)

    reduced_brightness_frame = cv2.addWeighted(blurred_frame, brightness_factor, dark_frame, 1 - brightness_factor, 0)

    cv2.imwrite(f'{MainMenuBackgroundDir}/frame{frame_count}.jpg', reduced_brightness_frame)
    frame_count += 1

cap.release()
cv2.destroyAllWindows()
