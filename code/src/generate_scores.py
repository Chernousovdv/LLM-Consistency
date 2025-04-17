import json
import random
import os

def save_scores_list(scores_list, folder_name):
    """Save the scores list configuration"""
    with open(os.path.join(folder_name, "scores.json"), "w") as f:
        json.dump(scores_list, f, indent=2)

def generate_random_scores_list(n=1, traits=None, order="01234"):
    """Generate random scores list for experiments"""
    if traits is None:
        traits = [
            "openness",
            "conscientiousness",
            "extraversion",
            "agreeableness",
            "neuroticism",
        ]
        traits = [traits[int(j)] for j in order]
    return [{trait: random.randint(1, 5) for trait in traits} for _ in range(n)]