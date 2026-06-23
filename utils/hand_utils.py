def count_fingers(hand_landmarks):
    tips = [8, 12, 16, 20]   # finger tips
    count = 0

    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1

    return count

def extract_features(hand_landmarks):
    features = []
    for lm in hand_landmarks:
        features.extend([lm.x, lm.y, lm.z])
    return features
