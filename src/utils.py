import os
import json


class ExperimentLogger:
    @staticmethod
    def save_results(data: dict, output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "a") as f:
            f.write(json.dumps(data) + "\n")

    @staticmethod
    def load_results(file_path: str) -> list[dict]:
        with open(file_path, "r") as f:
            return [json.loads(line) for line in f]
