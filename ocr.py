"""OCR module using pytesseract."""

import cv2
import pytesseract


class OCR:
    def extract_text(self, frame) -> str:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text.strip()
