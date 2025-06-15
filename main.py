"""Main orchestrator for the modular AI assistant."""

import argparse
import threading
import cv2

from object_detection import ObjectDetector
from face_recognition_module import FaceRecognizer
from ocr import OCR
from motion_detector import MotionDetector
from gpio_controller import GPIOController
from voice_assistant import VoiceAssistant
from event_logger import EventLogger
# Optional imports
try:
    from thermal_cam import ThermalCamera
except ImportError:
    ThermalCamera = None

try:
    from slam_module import SLAMModule
except ImportError:
    SLAMModule = None


def parse_args():
    parser = argparse.ArgumentParser(description="Modular AI Assistant")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    parser.add_argument("--detect", action="store_true", help="Enable object detection")
    parser.add_argument("--faces", action="store_true", help="Enable face recognition")
    parser.add_argument("--ocr", action="store_true", help="Enable OCR")
    parser.add_argument("--motion", action="store_true", help="Enable motion detection")
    parser.add_argument("--voice", action="store_true", help="Enable voice assistant")
    parser.add_argument("--thermal", action="store_true", help="Enable thermal camera")
    parser.add_argument("--slam", action="store_true", help="Enable SLAM")
    return parser.parse_args()


class CameraStream:
    """Handle real-time camera input."""

    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        if not self.capture.isOpened():
            raise RuntimeError("Camera not accessible")
        self.running = True
        self.frame = None
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                continue
            with self.lock:
                self.frame = frame

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.running = False
        self.thread.join()
        self.capture.release()


def main():
    args = parse_args()
    camera = CameraStream(args.camera)
    detector = ObjectDetector() if args.detect else None
    recognizer = FaceRecognizer() if args.faces else None
    ocr_engine = OCR() if args.ocr else None
    motion = MotionDetector() if args.motion else None
    gpio = GPIOController()
    voice = VoiceAssistant() if args.voice else None
    logger = EventLogger()
    thermal = ThermalCamera() if args.thermal and ThermalCamera else None
    slam = SLAMModule() if args.slam and SLAMModule else None

    try:
        while True:
            frame = camera.read()
            if frame is None:
                continue
            if detector:
                detections = detector.detect(frame)
                for det in detections:
                    cv2.rectangle(frame, det.box[:2], det.box[2:], (0, 255, 0), 2)
            if recognizer:
                faces = recognizer.recognize(frame)
                for name, box in faces:
                    cv2.rectangle(frame, box[:2], box[2:], (255, 0, 0), 2)
                    cv2.putText(frame, name, box[:2], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            if ocr_engine:
                text = ocr_engine.extract_text(frame)
                if text:
                    logger.log_event("ocr", text)
            if motion:
                if motion.detect(frame):
                    logger.log_event("motion", "Movement detected")
            if thermal:
                thermal.process(frame)
            if slam:
                slam.process(frame)
            cv2.imshow("Assistant", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
