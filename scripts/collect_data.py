import csv
import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from utils.feature_extractor import extract_features

LABEL = input("Enter gesture label: ")

csv_file = open("gesture_dataset.csv", "a", newline="")
writer = csv.writer(csv_file)

base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]
        features = extract_features(hand)

        writer.writerow([LABEL] + features)

        print("Saved:", LABEL)

    cv2.imshow("Collecting Data", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
csv_file.close()