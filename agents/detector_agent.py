# agents/detector_agent.py
from core.detector import Detector

class DetectorAgent:
    def __init__(self, cam_index=0, min_area=800):
        self.detector = Detector(cam_index=cam_index, min_area=min_area)
        # open camera immediately (or on first use)
        self.detector.open_camera()

    async def run_once(self):
        """
        Capture one frame and return detected obstacles.
        Returns: (frame, obstacles)
        """
        frame = self.detector.read_frame()
        obstacles = self.detector.detect_once(frame) if frame is not None else []
        return frame, obstacles

    def release(self):
        self.detector.release()
