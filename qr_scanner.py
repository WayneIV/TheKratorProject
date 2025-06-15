"""Barcode and QR code scanner using pyzbar."""

from typing import List
import cv2
from pyzbar import pyzbar


def scan_codes(frame) -> List[str]:
    barcodes = pyzbar.decode(frame)
    return [barcode.data.decode("utf-8") for barcode in barcodes]
