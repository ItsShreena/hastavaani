import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def _speak(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    if not text or text.strip() == "":
        return
    threading.Thread(target=_speak, args=(text,), daemon=True).start()