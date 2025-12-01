# core/tts.py
import pyttsx3
import threading

class TTS:
    def __init__(self, rate: int = 160, volume: float = 1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

    def _speak_blocking(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    def speak(self, text: str, async_mode: bool = True):
        """Speak text. By default runs in a thread to avoid blocking main loop."""
        if async_mode:
            t = threading.Thread(target=self._speak_blocking, args=(text,), daemon=True)
            t.start()
        else:
            self._speak_blocking(text)
