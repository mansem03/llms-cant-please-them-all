from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json
import pandas as pd


def save_jsonl(df: pd.DataFrame, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in df.to_dict(orient="records"):
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_run_summary(output_dir: Path, judge_provider: str, n_candidates: int, selected: pd.DataFrame, score_df: pd.DataFrame) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "datetime": datetime.now().isoformat(timespec="seconds"),
        "judge_provider": judge_provider,
        "n_candidates_per_topic": n_candidates,
        "num_topics": int(selected.shape[0]),
        "num_judgements": int(score_df.shape[0]),
        "average_selected_objective": float(selected["objective"].mean()) if not selected.empty else 0.0,
        "average_selected_mean_score": float(selected["mean_score"].mean()) if not selected.empty else 0.0,
        "average_selected_disagreement_range": float(selected["range_score"].mean()) if not selected.empty else 0.0,
    }
    (output_dir / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = f"""# Run Summary

Date: {summary['datetime']}

Judge provider: **{judge_provider}**

Topics processed: **{summary['num_topics']}**

Candidates per topic: **{n_candidates}**

Judgements produced: **{summary['num_judgements']}**

Average selected objective: **{summary['average_selected_objective']:.3f}**

Average selected mean score: **{summary['average_selected_mean_score']:.3f}**

Average selected disagreement range: **{summary['average_selected_disagreement_range']:.3f}**

Files generated:

- `submission.csv`
- `all_judge_scores.csv`
- `candidate_summary.csv`
- `selected_candidates.csv`
- `objective_distribution.png`
- `mean_vs_disagreement.png`
"""
    (output_dir / "run_summary.md").write_text(md, encoding="utf-8")
