# core/detector.py
import cv2
import numpy as np

class Detector:
    """Simple OpenCV-based detector returning bounding boxes of large contours."""

    def __init__(self, cam_index=0, min_area=800):
        self.cam_index = cam_index
        self.cap = None
        self.min_area = min_area

    def open_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.cam_index)
        return self.cap is not None and self.cap.isOpened()

    def read_frame(self):
        if not self.open_camera():
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def detect_once(self, frame):
        """
        Returns list of obstacles as dicts: {"bbox": (x,y,w,h), "area": area}
        Simple threshold + contour area filter approach.
        """
        if frame is None:
            return []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # blur to reduce noise
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        # adaptive threshold or simple threshold
        _, th = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        obstacles = []
        h, w = frame.shape[:2]
        for c in contours:
            area = cv2.contourArea(c)
            if area < self.min_area:
                continue
            x,y,ww,hh = cv2.boundingRect(c)
            # estimated relative size/distance proxy
            rel_size = ww * hh / (w*h)
            obstacles.append({"bbox": (int(x),int(y),int(ww),int(hh)), "area": area, "rel_size": rel_size})
        return obstacles

    def release(self):
        if self.cap:
            self.cap.release()
            self.cap = None
