# agents/llm_agent.py
import asyncio

class LLMAgent:
    def __init__(self, model_name="mock"):
        self.model_name = model_name

    async def describe_obstacles(self, obstacles):
        """
        Given a list of obstacles, return a short natural description.
        This is a mock. Replace with real LLM call if you want.
        """
        await asyncio.sleep(0.08)  # simulate latency
        if not obstacles:
            return "There are no obstacles ahead."
        # simple summary
        n = len(obstacles)
        large = sum(1 for o in obstacles if o["rel_size"] > 0.02)
        return f"Warning: detected {n} obstacle(s) ahead. {large} of them appear large."
