import requests
from utils.tts import speak

class DoctorAgent:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"

    def consult(self, user_input, lang="ta"):
        try:
            response = requests.post(
                self.ollama_url,
                json={"model": "mistral", "prompt": f"As a doctor, advise: {user_input}", "stream": False}
            )
            reply = response.json()["response"]
            print(f"🩺 Doctor: {reply}")
            speak(reply, lang)
            return reply
        except Exception as e:
            fallback = "Sorry, I couldn’t connect to the doctor AI. Please check vitals manually."
            print(f"❌ Ollama error: {e}. {fallback}")
            speak(fallback, lang)
            return fallback