import cv2
from ultralytics import YOLO
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os
import speech_recognition as sr
import threading

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Track announced objects
announced = set()
last_message = ""

# Speech recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    """Convert text to speech and play it."""
    global last_message
    try:
        last_message = text
        print(f"SPEAKING: {text}")
        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tmpfile = fp.name
        tts.save(tmpfile)
        audio = AudioSegment.from_mp3(tmpfile)
        play(audio)
        os.remove(tmpfile)
    except Exception as e:
        print("TTS error:", e)

def listen_for_commands():
    """Continuously listen for user voice commands in background."""
    global last_message
    while True:
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
                command = recognizer.recognize_google(audio).lower()
                print(f"COMMAND HEARD: {command}")

                if "repeat" in command and last_message:
                    speak(last_message)
                elif "stop" in command:
                    print("Stopping by voice command.")
                    os._exit(0)
        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            print("Voice command error:", e)

# Run voice command listener in background thread
threading.Thread(target=listen_for_commands, daemon=True).start()

# Open webcam
cap = cv2.VideoCapture(0)

print("Ready. Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    detected_objects = set()

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            detected_objects.add(label)

    print(f"Detected this frame: {detected_objects}")

    new_objects = detected_objects - announced
    if new_objects:
        for obj in new_objects:
            speak(f"I see {obj}")
        announced.update(new_objects)

    cv2.imshow("Smart Assistant", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
