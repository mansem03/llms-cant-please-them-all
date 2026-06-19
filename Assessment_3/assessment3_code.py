from __future__ import annotations

from pathlib import Path
import argparse
import pandas as pd

from src.config import Config
from src.data import load_topics, load_sample_submission_columns
from src.essay_generator import generate_template_candidates
from src.judges import build_judge
from src.selection import score_candidates, summarize_candidates, select_best, make_submission
from src.viz import plot_candidate_summary
from src.export import save_jsonl, write_run_summary


def parse_args():
    parser = argparse.ArgumentParser(description="LLMs - You Can't Please Them All student project pipeline")
    parser.add_argument("--judge", choices=["heuristic", "gemini", "ollama"], default=None, help="Override JUDGE_PROVIDER from .env")
    parser.add_argument("--n-candidates", type=int, default=None, help="Number of candidate essays per topic")
    parser.add_argument("--max-topics", type=int, default=None, help="Limit topics for testing. 0 means all topics")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = Config.from_env()
    if args.judge:
        cfg.judge_provider = args.judge
    if args.n_candidates is not None:
        cfg.n_candidates = args.n_candidates
    if args.max_topics is not None:
        cfg.max_topics = args.max_topics
    cfg.validate()

    topics_df, original_id_col, _ = load_topics(cfg.data_dir, max_topics=cfg.max_topics)
    submission_id_col, submission_essay_col = load_sample_submission_columns(cfg.data_dir)

    print(f"Loaded {len(topics_df)} topics")
    print(f"Judge provider: {cfg.judge_provider}")
    print(f"Candidates per topic: {cfg.n_candidates}")

    all_candidates = []
    for _, row in topics_df.iterrows():
        all_candidates.extend(
            generate_template_candidates(
                topic_id=str(row["id"]),
                topic=str(row["topic"]),
                n_candidates=cfg.n_candidates,
                seed=cfg.random_seed,
            )
        )

    judge = build_judge(
        provider=cfg.judge_provider,
        gemini_api_key=cfg.gemini_api_key,
        gemini_model=cfg.gemini_model,
        ollama_model=cfg.ollama_model,
        ollama_host=cfg.ollama_host,
    )

    score_df = score_candidates(all_candidates, judge)
    summary_df = summarize_candidates(score_df)
    selected_df = select_best(summary_df)
    submission = make_submission(selected_df, id_col=submission_id_col, essay_col=submission_essay_col)

    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    score_df.to_csv(cfg.output_dir / "all_judge_scores.csv", index=False)
    summary_df.to_csv(cfg.output_dir / "candidate_summary.csv", index=False)
    selected_df.to_csv(cfg.output_dir / "selected_candidates.csv", index=False)
    submission.to_csv(cfg.output_dir / "submission.csv", index=False)
    save_jsonl(score_df, cfg.output_dir / "all_judge_scores.jsonl")
    plot_candidate_summary(summary_df, cfg.output_dir)
    write_run_summary(cfg.output_dir, cfg.judge_provider, cfg.n_candidates, selected_df, score_df)

    print("\nDone. Files saved in outputs/")
    print("Main Kaggle file: outputs/submission.csv")
    print("Experiment files: outputs/all_judge_scores.csv, outputs/candidate_summary.csv, outputs/selected_candidates.csv")


if __name__ == "__main__":
    main()
