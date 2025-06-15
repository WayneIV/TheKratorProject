"""Simple voice interface wrapping STT and TTS libraries."""

try:
    import speech_recognition as sr
    import pyttsx3
except ImportError:  # pragma: no cover - optional deps for skeleton
    sr = None
    pyttsx3 = None


class VoiceInterface:
    """Handle microphone input and voice output."""

    def __init__(self):
        self.recognizer = sr.Recognizer() if sr else None
        self.engine = pyttsx3.init() if pyttsx3 else None

    def listen(self) -> str:
        """Return text captured from the microphone."""
        if not self.recognizer or not sr:
            return ""
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""

    def speak(self, text: str):
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
