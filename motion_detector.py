"""Simple motion detection using frame differencing."""

import cv2
import numpy as np


class MotionDetector:
    def __init__(self, threshold: int = 25):
        self.prev_gray = None
        self.threshold = threshold

    def detect(self, frame) -> bool:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_gray is None:
            self.prev_gray = gray
            return False
        diff = cv2.absdiff(self.prev_gray, gray)
        self.prev_gray = gray
        _, thresh = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)
        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return any(cv2.contourArea(c) > 500 for c in cnts)
