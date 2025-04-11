from gtts import gTTS
import os
import platform

def speak(text, lang='ta'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    system = platform.system()
    if system == "Windows":
        os.system("start output.mp3")
    elif system == "Darwin":
        os.system("afplay output.mp3")
    else:
        os.system("mpg123 output.mp3")

