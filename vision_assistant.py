import cv2
import pytesseract
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class DetectedObject:
    label: str
    coordinates: Tuple[int, int, int, int]


def read_text(image_path: str) -> str:
    """Extract text from an image using pytesseract."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()


def detect_faces(image_path: str) -> List[DetectedObject]:
    """Detect faces in an image using OpenCV's Haar cascades."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    results = [DetectedObject('face', (x, y, w, h)) for (x, y, w, h) in faces]
    return results


def detect_eyes(image_path: str) -> List[DetectedObject]:
    """Detect eyes in an image."""
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    results = [DetectedObject('eye', (x, y, w, h)) for (x, y, w, h) in eyes]
    return results


def skeptical_analysis(text: str) -> str:
    """Return a slightly skeptical response to extracted text."""
    if text:
        return f"I read: '{text}'. Are you sure this is accurate?"
    return "No text detected to analyze."



def detect_bodies(image_path: str) -> List[DetectedObject]:
    """Detect human bodies in an image."""
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
    results = [DetectedObject('body', (x, y, w, h)) for (x, y, w, h) in bodies]
    return results


def environment_metrics(image_path: str) -> dict:
    """Return simple metrics about the scene to showcase situational awareness."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = float(gray.mean())
    height, width = image.shape[:2]
    return {"width": width, "height": height, "brightness": brightness}



def main(image_path: str):
    print("Running vision analysis on", image_path)
    text = read_text(image_path)
    faces = detect_faces(image_path)
    bodies = detect_bodies(image_path)
    env = environment_metrics(image_path)

    print("Text found:", text)
    for item in faces:
        print("Face at", item.coordinates)
    for item in bodies:
        print("Body at", item.coordinates)
    print("Environment metrics:", env)
    print(skeptical_analysis(text))


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python vision_assistant.py <image>")
        sys.exit(1)
    main(sys.argv[1])
