from __future__ import annotations

from pathlib import Path
from typing import Tuple
import pandas as pd


POSSIBLE_ID_COLUMNS = ["id", "ID", "row_id", "essay_id"]
POSSIBLE_TOPIC_COLUMNS = ["topic", "prompt", "essay_topic", "question", "instruction"]


def _first_existing(columns, choices):
    lowered = {c.lower(): c for c in columns}
    for choice in choices:
        if choice in columns:
            return choice
        if choice.lower() in lowered:
            return lowered[choice.lower()]
    return None


def load_topics(data_dir: Path, max_topics: int = 0) -> Tuple[pd.DataFrame, str, str]:
    """Load Kaggle test topics.

    Returns a dataframe with standard columns: id, topic.
    If data/test.csv is missing, it creates a tiny sample so the code can run.
    """
    test_path = data_dir / "test.csv"
    if not test_path.exists():
        sample = pd.DataFrame(
            {
                "id": [0, 1, 2],
                "topic": [
                    "Is technology making students more independent or more dependent?",
                    "Should universities use AI tools to grade essays?",
                    "Can social media improve public discussion?",
                ],
            }
        )
        sample.to_csv(test_path, index=False)
        print("data/test.csv was not found, so a small demo test.csv was created.")
        print("Replace it with the Kaggle test.csv before your real experiment.")

    df = pd.read_csv(test_path)
    id_col = _first_existing(df.columns, POSSIBLE_ID_COLUMNS)
    topic_col = _first_existing(df.columns, POSSIBLE_TOPIC_COLUMNS)

    if id_col is None:
        id_col = df.columns[0]
    if topic_col is None:
        # Most Kaggle versions use columns similar to id/topic. If not, choose first non-id text-like column.
        non_id_cols = [c for c in df.columns if c != id_col]
        if not non_id_cols:
            raise ValueError("Could not find a topic/prompt column in test.csv")
        topic_col = non_id_cols[0]

    out = df[[id_col, topic_col]].rename(columns={id_col: "id", topic_col: "topic"}).copy()
    out["topic"] = out["topic"].astype(str).str.strip()
    if max_topics and max_topics > 0:
        out = out.head(max_topics)
    return out, id_col, topic_col


def load_sample_submission_columns(data_dir: Path):
    sample_path = data_dir / "sample_submission.csv"
    if sample_path.exists():
        sample = pd.read_csv(sample_path)
        if len(sample.columns) >= 2:
            return sample.columns[0], sample.columns[1]
    return "id", "essay"
