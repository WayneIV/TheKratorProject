"""Authentication utilities for secure command execution."""

from __future__ import annotations

import logging
import os
from typing import List

import cv2
import face_recognition
try:
    import speech_recognition as sr
except ImportError:  # pragma: no cover - optional dep
    sr = None


class SecurityLayer:
    """Provide basic face and voice authentication."""

    def __init__(self, faces_dir: str = "known_faces", passphrase: str = "open sesame") -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.passphrase = passphrase.lower()
        self.recognizer = sr.Recognizer() if sr else None
        self.face_encodings: List = []
        self._load_faces(faces_dir)

    # Face authentication -------------------------------------------------
    def _load_faces(self, directory: str) -> None:
        if not os.path.isdir(directory):
            self.logger.warning("Faces directory %s not found", directory)
            return
        for name in os.listdir(directory):
            path = os.path.join(directory, name)
            try:
                image = face_recognition.load_image_file(path)
                enc = face_recognition.face_encodings(image)
                if enc:
                    self.face_encodings.append(enc[0])
            except Exception as exc:  # pragma: no cover - optional
                self.logger.warning("Failed loading face %s: %s", path, exc)
        self.logger.info("Loaded %d authorized face(s)", len(self.face_encodings))

    def authenticate_face(self, frame) -> bool:
        """Return True if any known face is detected in ``frame``."""
        if not self.face_encodings:
            return False
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        for enc in encodings:
            matches = face_recognition.compare_faces(self.face_encodings, enc)
            if True in matches:
                return True
        return False

    # Voice authentication ------------------------------------------------
    def authenticate_voice(self, audio) -> bool:
        """Return True if ``audio`` contains the authorized passphrase."""
        if not self.recognizer:
            self.logger.warning("speech_recognition not installed")
            return False
        try:
            text = self.recognizer.recognize_google(audio).lower()
            self.logger.debug("Voice transcript: %s", text)
            return self.passphrase in text
        except sr.UnknownValueError:
            self.logger.warning("Speech not recognized")
        except Exception as exc:  # pragma: no cover - runtime failure
            self.logger.error("Voice auth failed: %s", exc)
        return False
