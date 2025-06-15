"""Object detection using YOLOv8 via the ultralytics package."""

from dataclasses import dataclass
from typing import List

import cv2
try:
    from ultralytics import YOLO
except ImportError:  # pragma: no cover - optional dependency
    YOLO = None


@dataclass
class Detection:
    label: str
    confidence: float
    box: tuple


class ObjectDetector:
    def __init__(self, model_path: str = "yolov8n.pt"):
        if YOLO is None:
            raise ImportError("ultralytics package not installed")
        self.model = YOLO(model_path)

    def detect(self, frame) -> List[Detection]:
        results = self.model(frame, verbose=False)[0]
        detections = []
        for box, conf, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
            x1, y1, x2, y2 = map(int, box)
            label = self.model.names[int(cls)]
            detections.append(Detection(label, float(conf), (x1, y1, x2, y2)))
        return detections
