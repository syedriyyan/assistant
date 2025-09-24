from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os

last_message = ""

def speak(text):
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
