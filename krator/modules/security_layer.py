"""Authentication and device trust management."""

from __future__ import annotations

import logging
import os
from typing import List

import cv2
import face_recognition
try:
    import speech_recognition as sr
except ImportError:  # pragma: no cover - optional
    sr = None


class SecurityLayer:
    """Simple face and voice authentication layer."""

    def __init__(self, faces_dir: str = "known_faces", passphrase: str = "open sesame") -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.passphrase = passphrase.lower()
        self.recognizer = sr.Recognizer() if sr else None
        self.face_encodings: List = []
        self._load_faces(faces_dir)

    def _load_faces(self, directory: str) -> None:
        if not os.path.isdir(directory):
            return
        for name in os.listdir(directory):
            path = os.path.join(directory, name)
            try:
                image = face_recognition.load_image_file(path)
                enc = face_recognition.face_encodings(image)
                if enc:
                    self.face_encodings.append(enc[0])
            except Exception:
                continue

    def authenticate_face(self, frame) -> bool:
        if not self.face_encodings:
            return False
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        for enc in encodings:
            matches = face_recognition.compare_faces(self.face_encodings, enc)
            if True in matches:
                return True
        return False

    def authenticate_voice(self, audio) -> bool:
        if not self.recognizer:
            return False
        try:
            text = self.recognizer.recognize_google(audio).lower()
            return self.passphrase in text
        except Exception:
            return False
