def build_sentence(tokens):

    if not tokens:
        return ""

    # -------------------------
    # 1. CLEAN TOKENS
    # -------------------------
    cleaned = [t for t in tokens if t not in ["-", None, ""]]

    if not cleaned:
        return ""

    # -------------------------
    # 2. REMOVE CONSECUTIVE DUPLICATES
    # -------------------------
    deduped = []
    for t in cleaned:
        if not deduped or deduped[-1] != t:
            deduped.append(t)

    # -------------------------
    # 3. IMPROVED MAPPING (STATIC + MOTION)
    # -------------------------
    sentence_map = {
        "HELLO": "Hello",
        "THANK_YOU": "Thank you",
        "THANK YOU": "Thank you",
        "YES": "Yes",
        "NO": "No",
        "OK": "Okay",
        "GOOD": "Good",
        "BAD": "Bad",
        "HELP": "Help me",
        "STOP": "Stop",
        "LOVE": "I love you",
        "BYE": "Bye"
    }

    words = []

    for token in deduped:
        if token in sentence_map:
            words.append(sentence_map[token])

    if not words:
        return ""

    # -------------------------
    # 4. NATURAL FLOW IMPROVEMENT
    # -------------------------
    sentence = " ".join(words)

    # Fix repeated word spacing issues
    sentence = sentence.replace("  ", " ").strip()

    # -------------------------
    # 5. SMART PUNCTUATION
    # -------------------------
    last_word = words[-1]

    if last_word in ["Help me", "Stop"]:
        sentence += "!"
    elif last_word in ["Bye", "Thank you", "Hello"]:
        sentence += "."
    else:
        sentence += "."

    # -------------------------
    # 6. FINAL FORMATTING
    # -------------------------
    if sentence:
        sentence = sentence[0].upper() + sentence[1:]

    return sentence