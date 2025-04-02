from src.experiment import PersonalityExperiment
from src.utils import ExperimentLogger


def main():
    true_scores = {"openness": 0.8, "conscientiousness": 0.4, "extraversion": 0.6}

    experiment = PersonalityExperiment(
        traits=list(true_scores.keys()), true_scores=true_scores
    )

    results = []
    for _ in range(10):
        trial_result = experiment.run_trial({"temperature": 0.7, "max_tokens": 500})
        results.append(trial_result)

    ExperimentLogger.save_results(results, "results/experiment.jsonl")


if __name__ == "__main__":
    main()
