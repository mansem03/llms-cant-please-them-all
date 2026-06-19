from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from tqdm import tqdm

from .essay_generator import CandidateEssay
from .judges import BaseJudge, JudgeResult


def score_candidates(candidates: List[CandidateEssay], judge: BaseJudge) -> pd.DataFrame:
    """Run every judge persona on every candidate essay."""
    rows = []
    for c in tqdm(candidates, desc="Judging candidates"):
        results: List[JudgeResult] = judge.judge(c.topic, c.essay)
        for r in results:
            rows.append(
                {
                    "topic_id": c.topic_id,
                    "topic": c.topic,
                    "candidate_id": c.candidate_id,
                    "strategy": c.strategy,
                    "judge_name": r.judge_name,
                    "score": float(r.score),
                    "reason": r.reason,
                    "essay": c.essay,
                    "word_count": len(c.essay.split()),
                }
            )
    return pd.DataFrame(rows)


def summarize_candidates(score_df: pd.DataFrame) -> pd.DataFrame:
    """Summarise judge disagreement for each candidate.

    Objective idea:
    - The Kaggle task is about disagreement between judges.
    - For a student report, we still keep a quality floor by including mean score.
    - objective = disagreement range + std + small mean bonus - low-quality penalty.
    """
    group_cols = ["topic_id", "topic", "candidate_id", "strategy", "essay", "word_count"]
    summary = (
        score_df.groupby(group_cols)
        .agg(
            mean_score=("score", "mean"),
            std_score=("score", "std"),
            min_score=("score", "min"),
            max_score=("score", "max"),
            judge_count=("score", "count"),
        )
        .reset_index()
    )
    summary["std_score"] = summary["std_score"].fillna(0)
    summary["range_score"] = summary["max_score"] - summary["min_score"]
    summary["quality_penalty"] = np.where(summary["mean_score"] < 4.0, 1.5, 0.0)
    summary["length_penalty"] = np.where((summary["word_count"] < 90) | (summary["word_count"] > 500), 0.5, 0.0)
    summary["objective"] = (
        summary["range_score"]
        + summary["std_score"]
        + 0.15 * summary["mean_score"]
        - summary["quality_penalty"]
        - summary["length_penalty"]
    )
    return summary.sort_values(["topic_id", "objective"], ascending=[True, False])


def select_best(summary_df: pd.DataFrame) -> pd.DataFrame:
    idx = summary_df.groupby("topic_id")["objective"].idxmax()
    selected = summary_df.loc[idx].copy().sort_values("topic_id")
    return selected


def make_submission(selected: pd.DataFrame, id_col: str = "id", essay_col: str = "essay") -> pd.DataFrame:
    sub = selected[["topic_id", "essay"]].rename(columns={"topic_id": id_col, "essay": essay_col}).copy()
    return sub
