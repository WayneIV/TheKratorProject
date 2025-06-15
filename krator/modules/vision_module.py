"""Camera utilities for object and face detection."""

from __future__ import annotations
import logging
import cv2


class VisionModule:
    """Basic wrapper around OpenCV capture."""

    def __init__(self, camera_index: int = 0) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise RuntimeError("Camera not accessible")

    def read_frame(self) -> cv2.Mat | None:
        """Read a frame from the camera."""
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None

    def close(self) -> None:
        """Release the camera resource."""
        self.cap.release()
