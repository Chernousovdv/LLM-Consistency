import json
import re
from typing import Dict, List
import pandas as pd


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
    def _fallback_parse(text: str, traits: List[str]) -> Dict[str, float]:
        """Parse personality scores from text using regex fallback (1-5 scale)."""
        scores = {}

        for trait in traits:
            # Case-insensitive search with score validation
            match = re.search(
                rf"{re.escape(trait)}['\"]?\s*[:=]\s*((?:[1-4](?:\.\d+)?|5(?:\.0+)?))",  # Updated pattern
                text,
                re.IGNORECASE,
            )
            if match:
                try:
                    score = float(match.group(1))
                    if 1 <= score <= 5:  # Validate before adding
                        scores[trait] = score
                except ValueError:
                    continue

        # Post-parsing validation
        missing_traits = [t for t in traits if t not in scores]
        if missing_traits:
            raise ValueError(f"Missing scores for traits: {', '.join(missing_traits)}")

        invalid_scores = {t: s for t, s in scores.items() if not 1 <= s <= 5}
        if invalid_scores:
            raise ValueError(f"Scores out of 1-5 range: {invalid_scores}")

        return scores


def calculate_row_differences_by_index(df1, df2, person_col="person"):
    """
    Calculate row-wise differences between df2 and corresponding rows in df1 using df1's index.

    Parameters:
    -----------
    df1 : DataFrame
        Reference DataFrame with n rows (index used for matching)
    df2 : DataFrame
        DataFrame with n*m rows containing a person_col that matches df1's index
    person_col : str
        Name of the column in df2 that corresponds to df1's index

    Returns:
    --------
    DataFrame
        A DataFrame with the same number of rows as df2, containing differences
        between df2 rows and their corresponding df1 rows, with person_col preserved
    """
    # Reset df1's index to make it a column for merging
    df1_reset = df1.reset_index()

    # Merge df2 with df1 to align corresponding rows
    merged = df2.merge(
        df1_reset, left_on=person_col, right_on="index", suffixes=("", "_ref")
    )

    # Get columns that exist in both dataframes (excluding the person column)
    common_cols = [col for col in df1.columns if col in df2.columns]

    # Calculate differences for each common column
    diff_data = {}
    for col in common_cols:
        diff_data[col] = merged[col] - merged[f"{col}_ref"]

    # Create the differences DataFrame
    diff_df = pd.DataFrame(diff_data)

    # Add back the person column
    diff_df[person_col] = merged[person_col]

    # Reorder columns to put person first
    cols = [person_col] + common_cols
    return diff_df[cols]


def create_comparison_df(scores_list, results):
    """
    Create and return comparison dataframes for true scores, predicted scores, and their differences.

    Parameters:
    -----------
    scores_list : list of dicts
        List containing true scores (ground truth) for each metric
    results : list of dicts
        List containing LLM results, each with an "llm_scores" key containing predicted scores

    Returns:
    --------
    tuple of DataFrames
        Returns (true_score_df, pred_score_df, delta_score_df) where:
        - true_score_df: DataFrame of ground truth scores
        - pred_score_df: DataFrame of predicted scores from LLM
        - delta_score_df: DataFrame of differences (predicted - true)
    """
    # Convert to DataFrames
    true_score_df = pd.DataFrame(scores_list)
    pred_score_df = pd.DataFrame([result for result in results])

    # Calculate differences (ensure DataFrames align properly)
    delta_score_df = calculate_row_differences_by_index(true_score_df, pred_score_df)

    return true_score_df, pred_score_df, delta_score_df
