import json
import re
from typing import Dict


class DataProcessor:
    @staticmethod
    def clean_description(text: str) -> str:
        return text.strip()

    @staticmethod
    def parse_scores(response: str, traits: list[str]) -> Dict[str, float]:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return DataProcessor._fallback_parse(response, traits)

    @staticmethod
    def _fallback_parse(text: str, traits: list[str]) -> Dict[str, float]:
        scores = {}
        for trait in traits:
            match = re.search(rf"{trait}['\"]?\s*:\s*([0-9.]+)", text)
            scores[trait] = float(match.group(1)) if match else 0.0
        return scores
