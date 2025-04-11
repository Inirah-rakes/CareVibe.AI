from utils.tts import speak
import random

class SocialAgent:
    def __init__(self):
        self.messages = {
            "ta": ["எல்லாம் நல்லா இருக்கா?", "ஒரு பாட்டு பாடவா?"],
            "hi": ["सब ठीक है?", "एक गाना सुनाएं?"],
            "te": ["అంతా బాగుందా?", "ఒక పాట పాడనా?"]
        }

    def cheer_up(self, lang="ta"):
        message = random.choice(self.messages[lang])
        print(f" Social: {message}")
        speak(message, lang)