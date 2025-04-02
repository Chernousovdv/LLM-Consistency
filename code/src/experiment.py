import uuid
import numpy as np
import json
import re
from scipy.stats import pearsonr
from typing import Dict, List, Tuple
from src.llm_integration import LLMClient
from config.settings import ExperimentSettings


class PersonalityExperiment:
    def __init__(self, traits: List[str], true_scores: Dict[str, float]):
        self.traits = traits
        self.true_scores = true_scores
        self.client = LLMClient()

    def run_trial(self, model_params: dict) -> Dict:
        trial_id = str(uuid.uuid4())

        # Description generation
        desc_prompt = self._generate_description_prompt()
        description = self.client.get_response(desc_prompt, model_params)

        # Score prediction
        score_prompt = self._generate_scoring_prompt(description)
        llm_response = self.client.get_response(score_prompt, model_params)
        llm_scores = self._parse_scores(llm_response)

        return self._calculate_metrics(llm_scores)

    def generate_prompt(self) -> str:
        """Generate prompt for personality description generation."""
        traits_str = (
            ", ".join(self.traits[:-1]) + f", and {self.traits[-1]}"
            if len(self.traits) > 1
            else self.traits[0]
        )

        prompt = (
            f"Describe a fictional person's personality and behavior in vivid detail. "
            f"Focus on showing (not telling) their levels of {traits_str} through:\n"
            f"- Specific actions they would take\n- Typical dialogue examples\n- Reactions to scenarios\n"
            f"Avoid numerical ratings or direct trait mentions. Use implicit characterization."
        )
        return prompt

    def _parse_scores(self, response: str) -> Dict[str, float]:
        """Parse and validate scores from LLM response"""
        try:
            # Attempt JSON parsing first
            scores = json.loads(response)
        except json.JSONDecodeError:
            # Fallback to regex extraction
            scores = {}
            for trait in self.traits:
                # Match patterns like "Openness: 0.85" or "'neuroticism': 0.4"
                match = re.search(
                    rf"""({re.escape(trait)}['"]?\s*[:=]\s*)(\d*\.?\d+)""", 
                    response,
                    re.IGNORECASE
                )
                if match:
                    scores[trait] = float(match.group(2))

        # Validate all traits are present and within range
        for trait in self.traits:
            score = scores.get(trait)
            if score is None:
                raise ValueError(f"Missing score for trait: {trait}")
            if not 0 <= score <= 1:
                raise ValueError(f"Invalid score {score} for {trait}. Must be 0-1")

        return scores

    def _calculate_metrics(self, llm_scores: Dict) -> Dict:
        true_values = [self.true_scores[t] for t in self.traits]
        llm_values = [llm_scores[t] for t in self.traits]

        return {
            "mae": np.mean(np.abs(np.array(true_values) - np.array(llm_values))),
            "correlation": pearsonr(true_values, llm_values)[0],
        }
