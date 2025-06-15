"""Voice command interface using SpeechRecognition and pyttsx3."""

import speech_recognition as sr
import pyttsx3


class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def listen(self) -> str:
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()
