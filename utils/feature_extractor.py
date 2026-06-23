import math

def extract_features(hand_landmarks):

    features = []

    # ----------------------------
    # BASIC LANDMARKS
    # ----------------------------
    for lm in hand_landmarks:
        features.append(lm.x)
        features.append(lm.y)
        features.append(lm.z)

    # ----------------------------
    # EXTRA FEATURES (IMPORTANT)
    # ----------------------------

    wrist = hand_landmarks[0]
    index_tip = hand_landmarks[8]
    middle_tip = hand_landmarks[12]
    ring_tip = hand_landmarks[16]
    pinky_tip = hand_landmarks[20]

    # palm openness (distance between fingers)
    def dist(a, b):
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

    spread = (
        dist(wrist, index_tip) +
        dist(wrist, middle_tip) +
        dist(wrist, ring_tip) +
        dist(wrist, pinky_tip)
    ) / 4

    features.append(spread)

    # finger vertical alignment (helps HELLO vs THANK YOU)
    features.append(index_tip.y - wrist.y)
    features.append(middle_tip.y - wrist.y)

    return features