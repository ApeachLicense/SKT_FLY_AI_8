from __future__ import annotations

import json
import os
import random
from typing import Dict, List, Protocol

from src.models.stage2 import Stage2Output


class Provider(Protocol):
    def generate(self, stage2: Stage2Output) -> List[Dict[str, object]]: ...


class MockProvider:
    def generate(self, stage2: Stage2Output) -> List[Dict[str, object]]:
        captions: List[Dict[str, object]] = []
        for frame in stage2.frames:
            emo = (
                "▲"
                if frame.intent_tags.intensity > 0.7
                else ("▼" if frame.intent_tags.intensity < 0.3 else "♪")
            )
            text = f"{frame.intent_tags.event_type} {emo}"
            captions.append(
                {
                    "start": frame.time_s,
                    "end": frame.time_s + 1.0,
                    "text": text,
                    "type": "music_event",
                    "style": {
                        "color": frame.style.color,
                        "font_size_pct": frame.style.font_size_pct,
                        "font_weight": frame.style.font_weight,
                        "font_width": frame.style.font_width,
                        "animation": frame.style.animation,
                        "display_mode": "overlay",
                    },
                }
            )
        return captions


class OpenAIProvider:
    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        try:
            import openai  # type: ignore
        except Exception as e:
            raise ImportError("openai not installed") from e
        self._openai = openai
        self._model = model

    def generate(self, stage2: Stage2Output) -> List[Dict[str, object]]:
        messages = [
            {
                "role": "system",
                "content": "한국어 SDH 자막 생성기. JSON only. Use ▲▼♪ symbols.",
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "intents": [
                            {
                                "event_type": f.intent_tags.event_type,
                                "start": f.time_s,
                                "end": f.time_s + 1.0,
                                "intensity": f.intent_tags.intensity,
                                "tension": f.intent_tags.harmony_tension,
                            }
                            for f in stage2.frames
                        ],
                        "require": "Return JSON array captions with start,end,text (ko, include ▲▼♪).",
                    },
                    ensure_ascii=False,
                ),
            },
        ]
        resp = self._openai.ChatCompletion.create(
            model=self._model, messages=messages, max_tokens=300, temperature=0.7
        )
        content = resp["choices"][0]["message"]["content"]
        try:
            data = json.loads(content)
            return data if isinstance(data, list) else []
        except Exception:
            return []


def get_provider() -> Provider:
    name = os.getenv("STAGE3_PROVIDER", "mock").lower()
    if name == "openai":
        model = os.getenv("STAGE3_OPENAI_MODEL", "gpt-3.5-turbo")
        try:
            return OpenAIProvider(model=model)
        except Exception:
            return MockProvider()
    return MockProvider()
