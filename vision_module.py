"""Vision component using OpenCV for basic camera access."""

from typing import Optional

import cv2


class VisionModule:
    """Minimal vision handler for image capture and processing."""

    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.capture: Optional[cv2.VideoCapture] = None

    def open(self):
        """Initialize the camera device."""
        self.capture = cv2.VideoCapture(self.camera_index)

    def read_frame(self):
        """Return the latest frame from the camera if available."""
        if self.capture is None:
            return None
        ret, frame = self.capture.read()
        return frame if ret else None

    def close(self):
        if self.capture is not None:
            self.capture.release()
            self.capture = None
