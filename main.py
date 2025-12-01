# main.py
import asyncio
import logging
from agents.detector_agent import DetectorAgent
from agents.llm_agent import LLMAgent
from core.tts import TTS
from memory.session import SessionMemory
import cv2
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger("detector_ai")

async def main_loop(interval=1.5, cam_index=0):
    detector_agent = DetectorAgent(cam_index=cam_index, min_area=900)
    llm_agent = LLMAgent()
    tts = TTS()
    memory = SessionMemory()

    logger.info("Starting assistive detection loop. Press Ctrl+C to stop.")
    try:
        while True:
            start = time.time()
            frame, obstacles = await detector_agent.run_once()
            # save to session memory
            memory.append({"time": time.time(), "count": len(obstacles)})
            # ask (mock) LLM for a description
            desc = await llm_agent.describe_obstacles(obstacles)
            logger.info("LLM description: %s", desc)
            # speak in background
            tts.speak(desc, async_mode=True)

            # optional: visual debug window (can be disabled)
            if frame is not None:
                # draw bboxes
                for o in obstacles:
                    x,y,w,h = o["bbox"]
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.putText(frame, desc, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                cv2.imshow("Detector (press q to quit)", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            elapsed = time.time() - start
            await asyncio.sleep(max(0, interval - elapsed))
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    finally:
        detector_agent.release()
        cv2.destroyAllWindows()
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main_loop())
