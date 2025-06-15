"""Speech input/output utilities."""

from __future__ import annotations
try:
    import speech_recognition as sr
    import pyttsx3
except ImportError:  # pragma: no cover - optional
    sr = None
    pyttsx3 = None


class VoiceInterface:
    """Handle microphone input and text-to-speech."""

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer() if sr else None
        self.engine = pyttsx3.init() if pyttsx3 else None

    def listen(self) -> str:
        """Return transcribed speech text."""
        if not self.recognizer or not sr:
            return ""
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""

    def speak(self, text: str) -> None:
        """Output text via speech engine."""
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
