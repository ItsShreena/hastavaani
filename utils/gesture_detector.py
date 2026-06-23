def detect_gesture(hand):

    lm = hand

    tips = [4, 8, 12, 16, 20]

    fingers = []

    wrist = lm[0]

    # ----------------------------
    # THUMB (WRIST-RELATIVE FIX)
    # ----------------------------
    if lm[4].x < lm[3].x:
        thumb = 1
    else:
        thumb = 0

    fingers.append(thumb)

    # ----------------------------
    # OTHER FINGERS (MORE STABLE)
    # ----------------------------
    for tip in tips[1:]:
        if lm[tip].y < lm[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    # ----------------------------
    # GESTURE SCORING SYSTEM
    # ----------------------------

    def score(match):
        return sum([1 if f == m else 0 for f, m in zip(fingers, match)])

    gestures = {
        "HELLO":      [1, 1, 1, 1, 1],
        "NO":         [0, 0, 0, 0, 0],
        "YES":        [1, 0, 0, 0, 0],
        "OK":         [0, 1, 1, 0, 0],
        "POINT":      [0, 1, 0, 0, 0],
        "HELP":       [1, 1, 1, 0, 0],
        "STOP":       [1, 1, 1, 1, 0],
        "CLEAR":      [0, 0, 0, 0, 0],
        "GOOD":[0,1,1,1,1],
        "LOVE":[1,0,1,0,1],
        "CALL":[1,0,0,0,1],
         "FOOD":[0,1,1,0,1]
}
    

    best_gesture = "-"
    best_score = 0

    # ----------------------------
    # PICK BEST MATCH (CONFIDENCE)
    # ----------------------------
    for name, pattern in gestures.items():
        s = score(pattern)

        if s > best_score:
            best_score = s
            best_gesture = name

    # ----------------------------
    # CONFIDENCE THRESHOLD
    # ----------------------------
    confidence = best_score / 5.0

    if confidence >= 0.8:
       return best_gesture, confidence
    else:
         return "-", 0.0