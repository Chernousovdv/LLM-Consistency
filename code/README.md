# LLM Personality Consistency Experiment

---

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/yourusername/llm-personality-consistency.git
cd llm-personality-consistency
```

### Install Dependencies
```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows

# Install required packages
pip install -r requirements.txt
```

---

## API Key Configuration
1. **Obtain an API Key** from Deepseek Console.
2. **Create a `.env` file** in the project root:
   ```bash
   echo "DEEPSEEK_API_KEY=your_api_key_here" > .env
   ```
3. **Keep this file private** by adding it to `.gitignore`:
   ```bash
   echo "\n.env" >> .gitignore
   ```

---

## Running Experiments

### Basic Execution
```python
from src.experiment import run_experiment

results = run_experiment(
    true_scores={
        "openness": 0.8,
        "conscientiousness": 0.4,
        "extraversion": 0.6
    },
    output_path="results/main_study.jsonl",
    num_trials=10
)
```

### Advanced Parameters
```python
run_experiment(
    ...,  
    desc_temperature=0.9,  # More creative descriptions
    score_temperature=0.2,  # More deterministic scoring
    max_tokens=1000,        # Longer responses
    top_p=0.95             # Nucleus sampling
)
```

---

## Data Storage Format

Experiment results are stored in **JSON Lines format (`.jsonl`)**, where each line represents a trial:
```json
{
  "trial_id": "550e8400-e29b-41d4-a716-446655440000",
  "true_scores": {"openness": 0.8, "conscientiousness": 0.4},
  "llm_scores": {"openness": 0.72, "conscientiousness": 0.38},
  "description": "John is an imaginative artist who...",
  "metrics": {
    "mae": 0.06,
    "correlation": 0.92
  },
  "prompts": {
    "description": "Describe a person showing openness...",
    "scoring": "Analyze this description and score..."
  }
}
```

---


## 🚀 Extending the Project

### 📌 Add a New Personality Model
1. **Define a new model** in `api_config.py`
2. **Update API client** in `llm_integration.py`
3. **Modify model selection logic** in `experiment.py`

### 📌 Implement Custom Metrics
```python
# src/experiment.py
def _calculate_metrics(self, llm_scores):
    return {
        ...,
        "custom_metric": calculate_custom_metric()
    }
```

---