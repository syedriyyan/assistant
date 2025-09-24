# app/speech_to_text.py
import speech_recognition as sr

def listen_for_command(timeout=5, phrase_time_limit=5):
    """Listen to the user and return recognized text (lowercase)."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("❌ Speech service error:", e)
        return None
