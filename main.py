import cv2
import mediapipe as mp
import time
import csv
import os
from datetime import datetime

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from utils.speech import speak
from utils.sentence_builder import build_sentence
from utils.gesture_detector import detect_gesture


# ----------------------------
# SETTINGS
# ----------------------------
STABLE_FRAMES = 8
BUFFER_SIZE = 5
WORD_PAUSE = 1.5

# ----------------------------
# CSV LOGGING
# ----------------------------
CSV_FILE = "conversion_log.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Timestamp",
            "Gesture",
            "Sentence"
        ])
# ----------------------------
# MEDIAPIPE SETUP
# ----------------------------
base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)


# ----------------------------
# CAMERA
# ----------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Camera not accessible")
    exit()


# ----------------------------
# STATE
# ----------------------------
start_time = time.time()

gesture_buffer = []
gesture_freq = {}

sentence_tokens = []
history = []

gesture_count = 0
sentence_count = 0

stable_gesture = "-"
stable_count = 0

last_gesture_time = time.time()
status = "Ready"

motion_history = []
MOTION_BUFFER = 8

confidence = 0.0
gesture = "-"


# ----------------------------
# MOTION FUNCTIONS
# ----------------------------
def detect_bye_motion(history):
    if len(history) < 6:
        return False
    xs = [p[0] for p in history]
    return (max(xs) - min(xs)) > 0.15


def detect_thankyou_motion(history):
    if len(history) < 6:
        return False
    ys = [p[1] for p in history]
    return (ys[-1] - ys[0]) > 0.12


# ----------------------------
# WINDOW
# ----------------------------
window_name = "HastaVaani - Sentence Mode"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)


# ----------------------------
# MAIN LOOP
# ----------------------------
while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    raw_gesture = "-"
    motion_gesture = "-"

    # ----------------------------
    # HAND DETECTION
    # ----------------------------
    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        # ---------------- motion tracking ----------------
        wrist = hand[0]
        motion_history.append((wrist.x, wrist.y))

        if len(motion_history) > MOTION_BUFFER:
            motion_history.pop(0)

        # ---------------- static gesture ----------------
        out = detect_gesture(hand)

        # safe unpacking
        if isinstance(out, tuple):
            raw_gesture, confidence = out
        else:
            raw_gesture = out
            confidence = 0.0

        if raw_gesture != "-":
            gesture_buffer.append(raw_gesture)

            if len(gesture_buffer) > BUFFER_SIZE:
                gesture_buffer.pop(0)

            gesture = max(set(gesture_buffer), key=gesture_buffer.count)
        else:
            gesture = "-"
            gesture_buffer.clear()

        # draw landmarks
        h, w, _ = frame.shape

        for lm in hand:
            cx = int(lm.x * w)
            cy = int(lm.y * h)
            cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

    else:
        gesture = "-"
        confidence = 0.0
        gesture_buffer.clear()
        motion_history.clear()

    # ----------------------------
    # MOTION OVERRIDE
    # ----------------------------
    if detect_bye_motion(motion_history):
        motion_gesture = "BYE"

    elif detect_thankyou_motion(motion_history):
        motion_gesture = "THANK_YOU"

    if motion_gesture != "-":
        gesture = motion_gesture
        confidence = 1.0


    # ----------------------------
    # STABILITY CHECK
    # ----------------------------
    if gesture != "-" and gesture == stable_gesture:
        stable_count += 1
    else:
        stable_gesture = gesture
        stable_count = 1


    # ----------------------------
    # ACCEPT GESTURE
    # ----------------------------
    if stable_count >= STABLE_FRAMES:

        if not sentence_tokens or sentence_tokens[-1] != gesture:
            sentence_tokens.append(gesture)
            gesture_count += 1

            gesture_freq[gesture] = gesture_freq.get(gesture, 0) + 1

        last_gesture_time = time.time()
        stable_count = 0
        status = "Gesture Locked"


    # ----------------------------
    # SPEECH
    # ----------------------------
    now = time.time()

    if sentence_tokens and (now - last_gesture_time) > WORD_PAUSE:

        sentence = build_sentence(sentence_tokens)

        if sentence:
            history.append(sentence)
            sentence_count += 1

            status = "Speaking"
            speak(sentence)

        sentence_tokens = []
        status = "Ready"


    # ----------------------------
    # ANALYTICS
    # ----------------------------
    session_duration = int(time.time() - start_time)

    most_used = "-"
    if gesture_freq:
        most_used = max(gesture_freq, key=gesture_freq.get)


    # ----------------------------
    # UI
    # ----------------------------
    cv2.putText(frame, f"Gesture: {gesture}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.putText(frame, f"Confidence: {int(confidence * 100)}%", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.putText(frame, f"Status: {status}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.putText(frame, f"Tokens: {' '.join(sentence_tokens)}", (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.putText(frame, f"Session: {session_duration}s", (400, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, f"Most Used: {most_used}", (400, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.putText(frame, f"Gestures: {gesture_count}", (400, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"Sentences: {sentence_count}", (400, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, "Press C to clear | ESC to exit", (20, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

    # ----------------------------
    # HISTORY DISPLAY
    # ----------------------------
    cv2.putText(
        frame,
        "History:",
        (20, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    for i, item in enumerate(history[-5:]):
        cv2.putText(
            frame,
            item,
            (20, 250 + i * 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow(window_name, frame)

    key = cv2.waitKey(1) & 0xFF

    # CLEAR
    if key == ord('c'):
        history.clear()
        sentence_tokens.clear()
        gesture_freq.clear()
        print("History cleared.")

    # EXIT
    if key == 27:
        break


# ----------------------------
# CLEANUP
# ----------------------------
cap.release()
cv2.destroyAllWindows()
