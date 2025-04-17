from datetime import datetime
from typing import List, Dict
import json
import os
from src.utils import ExperimentLogger


class ResultExporter:
    @staticmethod
    def convert_results(jsonl_path: str, txt_path: str) -> None:
        """Convert JSONL results to formatted text report with display and save."""
        results = ExperimentLogger.load_results(jsonl_path)
        report = ResultExporter._generate_report(results)
        
        # Display in console
        print(report)
        
        # Save to text file
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(report)

    @staticmethod
    def _generate_report(results: List[Dict]) -> str:
        """Generate formatted text report from results data."""
        report = []
        
        # Header
        report.append("=" * 60)
        report.append(f"Personality Experiment Results Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Trials: {len(results)}")
        report.append("=" * 60 + "\n")

        # Trial details
        for idx, trial in enumerate(results, 1):
            report.append(f"Trial #{idx}")
            report.append("-" * 50)
            report.append(f"ID: {trial['trial_id']}")
            
            report.append("\n[Description Prompt]")
            report.append(trial['desc_prompt'])
            
            report.append("\n[Generated Description]")
            report.append(trial['llm_description'])
            
            report.append("\n[LLM Response]")
            report.append(trial['llm_response'])
            
            report.append("\n[Parsed Scores]")
            for trait, score in trial['llm_scores'].items():
                report.append(f"- {trait.capitalize()}: {score:.2f}")
            
            report.append("\n" + "=" * 60 + "\n")

        return "\n".join(report)

# Usage example:
ResultExporter.convert_results(
    jsonl_path="results/experiment.jsonl",
    txt_path="reports/experiment_summary.txt"
)