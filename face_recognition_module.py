"""Face detection and recognition using face_recognition library."""

import os
from typing import List, Tuple

import cv2
import face_recognition


class FaceRecognizer:
    def __init__(self, known_dir: str = "known_faces"):
        self.known_encodings = []
        self.known_names = []
        if os.path.isdir(known_dir):
            for name in os.listdir(known_dir):
                path = os.path.join(known_dir, name)
                image = face_recognition.load_image_file(path)
                enc = face_recognition.face_encodings(image)
                if enc:
                    self.known_encodings.append(enc[0])
                    self.known_names.append(os.path.splitext(name)[0])

    def recognize(self, frame) -> List[Tuple[str, Tuple[int, int, int, int]]]:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)
        results = []
        for enc, box in zip(encodings, boxes):
            matches = face_recognition.compare_faces(self.known_encodings, enc)
            name = "Unknown"
            if True in matches:
                idx = matches.index(True)
                name = self.known_names[idx]
            top, right, bottom, left = box
            results.append((name, (left, top, right, bottom)))
        return results
