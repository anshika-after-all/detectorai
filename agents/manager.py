import asyncio

class AgentManager:
    def __init__(self, detector_agent, llm_agent, tts, memory):
        self.detector = detector_agent
        self.llm = llm_agent
        self.tts = tts
        self.memory = memory

    async def sequential_run(self):
        """Detector -> LLM -> TTS"""
        obstacles = await self.detector.run()
        if not obstacles:
            text = "No obstacles detected."
        else:
            text = f"Detected {len(obstacles)} obstacle(s)."

        llm_out = await self.llm.run(text, memory=self.memory)
        self.tts.speak(llm_out)
        return llm_out

    async def loop_run(self, interval=1.0):
        while True:
            await self.sequential_run()
            await asyncio.sleep(interval)
