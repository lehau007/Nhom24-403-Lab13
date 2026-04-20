from __future__ import annotations

import os
from dataclasses import dataclass

import google.generativeai as genai

from .incidents import STATE
from .tracing import langfuse_context, observe


@dataclass
class GeminiUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class GeminiResponse:
    text: str
    usage: GeminiUsage
    model: str


class GeminiLLM:
    """Real LLM client using Google Gemini API.

    Drop-in replacement for FakeLLM — returns the same
    GeminiResponse/GeminiUsage shape that agent.py expects
    (attributes: .text, .usage.input_tokens, .usage.output_tokens, .model).
    """

    def __init__(self, model: str = "gemini-2.0-flash") -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. "
                "Add it to your .env file: GEMINI_API_KEY=your-key-here"
            )
        genai.configure(api_key=api_key)
        self.model_name = model
        self.client = genai.GenerativeModel(model)

    @observe(as_type="generation")
    def generate(self, prompt: str) -> GeminiResponse:
        # ── cost_spike simulation: inflate prompt to burn more tokens ──
        if STATE["cost_spike"]:
            prompt = prompt + ("\n[PADDING] " * 200)

        response = self.client.generate_content(prompt)

        # Extract token counts from usage_metadata
        usage_meta = response.usage_metadata
        input_tokens = getattr(usage_meta, "prompt_token_count", 0) or 0
        output_tokens = getattr(usage_meta, "candidates_token_count", 0) or 0

        # Report model + token usage to Langfuse so cost is calculated
        langfuse_context.update_current_observation(
            model=self.model_name,
            usage={"input": input_tokens, "output": output_tokens},
        )

        return GeminiResponse(
            text=response.text,
            usage=GeminiUsage(input_tokens=input_tokens, output_tokens=output_tokens),
            model=self.model_name,
        )
