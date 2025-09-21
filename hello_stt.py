import speech_recognition as sr

# Create a recognizer object
recognizer = sr.Recognizer()

# Use the default system microphone
with sr.Microphone() as source:
    print("🎤 Say something... (speak clearly)")
    audio = recognizer.listen(source)  # listen until silence

try:
    # Use Google Web Speech API (requires internet)
    text = recognizer.recognize_google(audio)
    print("✅ You said:", text)
except sr.UnknownValueError:
    print("❌ Sorry, I could not understand what you said.")
except sr.RequestError as e:
    print("❌ Could not connect to the service; check internet connection.", e)
