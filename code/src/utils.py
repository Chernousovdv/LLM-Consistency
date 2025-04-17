import os
import json
import random


class ExperimentLogger:
    @staticmethod
    def save_results(data: list[dict], output_path: str):
        """Save trial results in valid JSONL format."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            for entry in data:
                json_line = json.dumps(entry, ensure_ascii=False)
                f.write(json_line + "\n")

    @staticmethod
    def load_results(file_path: str) -> list[dict]:
        """Load results from JSONL file."""
        results = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                results.append(json.loads(line))
        return results


def create_numbered_folder(base_name="results/run"):
    """Create a new numbered folder in sequence"""
    i = 1
    while True:
        folder_name = f"{base_name}_{i}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            return folder_name
        i += 1
