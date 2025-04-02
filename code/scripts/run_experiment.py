from src.experiment import PersonalityExperiment
from src.utils import ExperimentLogger


def main():
    true_scores = {"openness": 2, "conscientiousness": 3, "extraversion": 4}

    experiment = PersonalityExperiment(
        traits=list(true_scores.keys()), true_scores=true_scores
    )

    results = []
    for _ in range(1):
        trial_result = experiment.run_trial({"temperature": 0.7, "max_tokens": 1000})
        results.append(trial_result)

    ExperimentLogger.save_results(results, "results/experiment.jsonl")


if __name__ == "__main__":
    main()
