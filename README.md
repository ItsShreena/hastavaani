#  HastaVaani — AI-Powered Sign Language Communication Assistant
 
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>
> **HastaVaani** (हस्तवाणी) — *"Hasta"* means hand, *"Vaani"* means voice.
 
### The Problem
 
Over 63 million people in India alone live with significant hearing or speech impairment. For many of them, sign language is the primary — and often only — means of natural communication. Yet most people around them don't understand it, creating an everyday barrier in hospitals, schools, workplaces, and public spaces.
 
Existing solutions are either too expensive, require specialised hardware, or depend on a human interpreter being physically present. **HastaVaani was built to remove that dependency** — giving individuals a portable, affordable, and instant voice using nothing more than a webcam and a laptop.
 
### Who It's For
 
- 🧏 **Deaf and hard-of-hearing individuals** who use sign language to communicate
- 🗣️ **Non-verbal or speech-impaired users** who rely on hand gestures
- 🏥 **Healthcare & support workers** who need a quick communication bridge with patients
- 🏫 **Educators and students** exploring assistive technology and AI accessibility tools
### How It Works
 
HastaVaani processes each webcam frame through a three-stage pipeline:
 
```
Webcam Frame  →  Hand Landmark Detection  →  Gesture Classification  →  Sentence Building  →  Speech Output
    (OpenCV)          (MediaPipe, 21 pts)      (Rules + Random Forest)     (sentence_builder)      (pyttsx3)
```
 
1. **Capture** — OpenCV reads frames from the webcam in real time.
2. **Detect** — MediaPipe identifies 21 hand keypoints (landmarks) per frame, tracking the precise position of every finger joint.
3. **Classify** — A combination of rule-based logic and a trained Random Forest model maps landmark geometry to a named gesture (e.g. `HELLO`, `STOP`, `LOVE`). Motion gestures like `BYE` additionally track landmark movement across frames.
4. **Build** — Stable, confirmed gestures are passed to the sentence builder, which groups tokens into natural, readable sentences.
5. **Speak** — The completed sentence is fed to `pyttsx3` for immediate offline text-to-speech playback, with no internet connection required.
---
 
## 📖 Table of Contents
 
- [Overview](#-overview)
- [Features](#-features)
- [Supported Gestures](#-supported-gestures)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Session Analytics](#-session-analytics)
- [CSV Logging](#-csv-logging)
- [Contributing](#-contributing)
- [License](#-license)
---
 
## 🧠 Overview
 
HastaVaani is an AI-powered sign language communication assistant that uses a webcam to detect hand gestures in real time. Recognized gestures are assembled into meaningful sentences, spoken aloud via text-to-speech, and logged to a CSV file for session review. A companion Streamlit dashboard provides visual analytics.
 
---
 
## ✨ Features
 
- 🎥 **Real-time webcam hand tracking** using OpenCV
- 🖐️ **Hand landmark detection** powered by MediaPipe
- 🤖 **Rule-based & ML gesture recognition** via a trained Random Forest model
- 🗣️ **Text-to-speech output** using `pyttsx3`
- 🧩 **Sentence building** from sequential gesture tokens
- 📊 **Session analytics** — gesture counts, most-used gesture, session duration
- 📁 **CSV logging** of all recognized gestures and sentences
- 🖥️ **Streamlit dashboard** for visual session review
---
 
## 🤚 Supported Gestures
 
### Static Gestures
| Gesture | Description |
|---------|-------------|
| `HELLO` | Open palm facing forward |
| `YES` | Fist nodding motion (held) |
| `NO` | Index finger wag |
| `OK` | Thumb and index forming a circle |
| `POINT` | Index finger extended forward |
| `HELP` | Thumb up on flat palm |
| `STOP` | Open palm facing outward |
| `GOOD` | Thumbs up |
| `LOVE` | Sign language "I Love You" hand |
| `CALL` | Phone hand (thumb and pinky extended) |
| `FOOD` | Fingers pinched to mouth |
 
### Motion-Based Gestures
| Gesture | Description |
|---------|-------------|
| `BYE` | Waving hand motion |
| `THANK_YOU` | Hand moving outward from chin |
 
---
 
## 🛠️ Tech Stack
 
| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core language |
| **OpenCV** | Webcam capture & frame processing |
| **MediaPipe** | Hand landmark detection (21 keypoints) |
| **NumPy** | Numerical operations on landmark data |
| **pyttsx3** | Offline text-to-speech engine |
| **Streamlit** | Interactive analytics dashboard |
| **scikit-learn** | Random Forest gesture classifier |
| **CSV** | Lightweight session logging |
 
---
 
## 📁 Project Structure
 
```
HastaVaani/
│
├── main.py                  # Main camera-based gesture recognition app
├── app.py                   # Streamlit dashboard UI
├── train_model.py           # Random Forest model training script
├── hand_landmarker.task     # MediaPipe hand landmark model file
├── conversion_log.csv       # Auto-generated gesture/sentence log
├── requirements.txt         # Python dependencies
│
└── utils/
    ├── gesture_detector.py  # Detects gestures from hand landmarks
    ├── sentence_builder.py  # Converts gesture tokens into sentences
    ├── speech.py            # Text-to-speech interface
    └── hand_utils.py        # Helper functions for landmark features
```
 
---
 
## 🚀 Getting Started
 
### Prerequisites
 
- Python 3.8 or higher
- A working webcam
- pip (Python package manager)
### Installation
 
**1. Clone the repository**
```bash
git clone https://github.com/your-username/HastaVaani.git
cd HastaVaani
```
 
**2. Create and activate a virtual environment**
 
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
 
On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```
 
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
 
> ⚠️ **Note:** This is a Python project. Do **not** use `npm run dev` — it will not work here.
 
---
 
## 🎮 Usage
 
### Run the Main Gesture Recognition App
 
```bash
python main.py
```
 
This launches the webcam feed, starts detecting hand gestures in real time, builds sentences from recognized gestures, and speaks them aloud.
 
**Controls during the session:**
- Press `S` — Speak the current sentence
- Press `C` — Clear the current sentence buffer
- Press `Q` — Quit the application
### Run the Streamlit Dashboard
 
```bash
streamlit run app.py
```
 
Opens an interactive browser dashboard showing session logs, gesture frequency charts, and conversion history from `conversion_log.csv`.
 
### Train the Gesture Model (Optional)
 
```bash
python train_model.py
```
 
Retrains the Random Forest classifier on gesture landmark data. Use this if you add new gestures or collect new training samples.
 
---
 
## 📊 Session Analytics
 
At the end of each session, HastaVaani displays a summary:
 
```
─────────────────────────────────────
       SESSION SUMMARY
─────────────────────────────────────
 Gestures Detected   :  42
 Sentences Spoken    :  8
 Most Used Gesture   :  HELLO
 Session Duration    :  00:04:37
─────────────────────────────────────
```
 
---
 
## 📁 CSV Logging
 
Every recognized gesture and sentence is automatically logged to `conversion_log.csv`:
 
```csv
timestamp,gesture,sentence,confidence
2025-06-20 10:32:01,HELLO,"Hello there!",0.94
2025-06-20 10:32:08,HELP,"Can you help me?",0.91
2025-06-20 10:32:15,THANK_YOU,"Thank you.",0.88
```
 
This file is created automatically on first run and appended to on every subsequent session.
 
---
 
## 🤝 Contributing
 
Contributions are welcome! Here's how you can help:
 
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/add-new-gesture`)
3. **Commit** your changes (`git commit -m 'Add WATER gesture support'`)
4. **Push** to the branch (`git push origin feature/add-new-gesture`)
5. **Open** a Pull Request
### Ideas for Contribution
- Add more ISL (Indian Sign Language) gestures
- Improve motion-gesture detection accuracy
- Add multi-hand support
- Build a gesture data collection tool
- Improve the Streamlit dashboard with real-time feed
---
 
## 📄 License
 
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
 

