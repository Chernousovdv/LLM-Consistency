import uuid
import numpy as np
import json
import re
from scipy.stats import pearsonr
from typing import Dict, List, Tuple
from src.llm_integration import LLMClient
from pathlib import Path
from jinja2 import Template


class PersonalityExperiment:
    def __init__(
        self,
        traits: List[str],
        true_scores: Dict[str, int],
        description_prompt="prompt1.jinja",
        scoring_prompt="prompt1.jinja",
    ):
        self.traits = traits
        self.true_scores = true_scores
        self.client = LLMClient()

        # Load prompt templates
        self.prompt_templates = {
            "description": Template((Path("prompts/describing") / description_prompt).read_text()),
            "scoring": Template((Path("prompts/scoring") / scoring_prompt).read_text()),
        }

    def _generate_description_prompt(self) -> str:
        traits_with_scores = "\n".join(
            f"- {trait.capitalize()}: {score}"
            for trait, score in self.true_scores.items()
        )
        return self.prompt_templates["description"].render(
            traits_with_scores=traits_with_scores
        )

    def _generate_scoring_prompt(self, description: str) -> str:
        traits_str = ", ".join(self.traits)
        example_traits = {trait.lower(): 3 for trait in self.traits[:2]}
        example_json = json.dumps(example_traits, indent=2)

        return self.prompt_templates["scoring"].render(
            traits_str=traits_str, description=description, example_json=example_json
        )

    def run_trial(self, model_params: dict) -> Dict:
        trial_id = str(uuid.uuid4())

        # Description generation
        desc_prompt = self._generate_description_prompt()
        description = self.client.get_response(desc_prompt, model_params)

        # Score prediction
        score_prompt = self._generate_scoring_prompt(description)
        llm_response = self.client.get_response(
            score_prompt, {"temperature": 0, "max_tokens": 200}
        )
        llm_scores = self._parse_scores(llm_response)

        return {
            "trial_id": trial_id,
            "true_scores": self.true_scores,
            "desc_prompt": desc_prompt,
            "llm_description": description,
            "score_prompt": score_prompt,
            "llm_response": llm_response,
            "llm_scores": llm_scores,
            "model_params": model_params,
        }

    def _parse_scores(self, response: str) -> Dict[str, float]:
        """Parse and validate scores from LLM response (1-5 scale)"""
        scores = {}

        try:
            scores = json.loads(response)
        except json.JSONDecodeError:
            # Regex fallback for 1-5 scores (integers or decimals)
            for trait in self.traits:
                match = re.search(
                    rf"""({re.escape(trait)}['"]?\s*[:=]\s*)([1-5](?:\.\d+)?)""",  # Changed pattern
                    response,
                    re.IGNORECASE,
                )
                if match:
                    scores[trait] = float(match.group(2))

        # Validate scores
        for trait in self.traits:
            score = scores.get(trait)
            if score is None:
                raise ValueError(f"Missing score for trait: {trait}")
            if not 1 <= score <= 5:
                raise ValueError(f"Invalid score {score} for {trait}. Must be 1-5")

        return scores
