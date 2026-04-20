from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE
from .tracing import langfuse_context, observe


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


class FakeLLM:
    def __init__(self, model: str = "gemini-2.0-flash") -> None:
        self.model = model

    @observe(as_type="generation")
    def generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.15)
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4
        answer = (
            "Starter answer. Teams should improve this output logic and add better quality checks. "
            "Use retrieved context and keep responses concise."
        )

        # Report model + token usage to Langfuse so cost is calculated
        langfuse_context.update_current_observation(
            model=self.model,
            usage={"input": input_tokens, "output": output_tokens},
        )

        return FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)
