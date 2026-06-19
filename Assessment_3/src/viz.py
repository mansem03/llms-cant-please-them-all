from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def _candidate_label(row: pd.Series) -> str:
    topic_id = row.get("topic_id", "")
    candidate_id = row.get("candidate_id", "")
    strategy = str(row.get("strategy", "")).replace("_", " ").title()

    if strategy and strategy.lower() != "nan":
        return f"T{topic_id}-C{candidate_id}\n{strategy}"

    return f"Candidate {candidate_id}"


def plot_candidate_summary(summary: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    if summary.empty:
        return

    # Make sure numeric columns are valid
    summary = summary.copy()
    summary["objective"] = pd.to_numeric(summary["objective"], errors="coerce")
    summary["mean_score"] = pd.to_numeric(summary["mean_score"], errors="coerce")
    summary["range_score"] = pd.to_numeric(summary["range_score"], errors="coerce")

    summary = summary.dropna(subset=["objective", "mean_score", "range_score"])

    if summary.empty:
        return

    # =====================================================
    # Graph 1: Candidate Objective Scores
    # Better than histogram when candidate number is small
    # =====================================================
    plot_df = summary.sort_values("objective", ascending=False).reset_index(drop=True)

    labels = [_candidate_label(row) for _, row in plot_df.iterrows()]
    objective_scores = plot_df["objective"]

    fig_width = max(9, len(plot_df) * 1.5)
    fig, ax = plt.subplots(figsize=(fig_width, 6))

    bars = ax.bar(labels, objective_scores)

    ax.set_title(
        "Candidate Objective Scores",
        fontsize=18,
        fontweight="bold",
        pad=18
    )

    ax.text(
        0.5,
        1.02,
        "Direct comparison is clearer than a histogram for small candidate sets.",
        transform=ax.transAxes,
        ha="center",
        fontsize=11,
        style="italic"
    )

    ax.set_xlabel("Candidate", fontsize=13, fontweight="bold")
    ax.set_ylabel("Objective Score", fontsize=13, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    max_y = max(objective_scores.max() * 1.20, 1)
    ax.set_ylim(0, max_y)

    for bar, value in zip(bars, objective_scores):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )

    ax.tick_params(axis="x", labelrotation=20)
    plt.tight_layout()

    # Save old filename so your project still works
    plt.savefig(output_dir / "objective_distribution.png", dpi=220)

    # Save clearer extra filename
    plt.savefig(output_dir / "ranked_objective_scores.png", dpi=220)

    plt.close()

    # =====================================================
    # Graph 2: Mean Judge Score vs Judge Disagreement
    # With candidate labels and explanation
    # =====================================================
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        summary["mean_score"],
        summary["range_score"],
        s=100,
        alpha=0.85,
        edgecolors="black",
        linewidths=0.7
    )

    ax.set_title(
        "Mean Judge Score vs Judge Disagreement",
        fontsize=18,
        fontweight="bold",
        pad=18
    )

    ax.text(
        0.5,
        1.02,
        "Higher disagreement means judges were less consistent.",
        transform=ax.transAxes,
        ha="center",
        fontsize=11,
        style="italic"
    )

    ax.set_xlabel("Mean Judge Score", fontsize=13, fontweight="bold")
    ax.set_ylabel("Judge Disagreement Range", fontsize=13, fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.35)

    x = summary["mean_score"]
    y = summary["range_score"]

    x_pad = max(0.05, (x.max() - x.min()) * 0.30)
    y_pad = max(0.20, (y.max() - y.min()) * 0.30)

    ax.set_xlim(x.min() - x_pad, x.max() + x_pad)
    ax.set_ylim(max(0, y.min() - y_pad), y.max() + y_pad)

    for i, row in summary.reset_index(drop=True).iterrows():
        label = (
            f"{_candidate_label(row)}\n"
            f"Mean: {row['mean_score']:.2f}\n"
            f"Range: {row['range_score']:.1f}"
        )

        offset = (15, 15) if i % 2 == 0 else (-130, -60)

        ax.annotate(
            label,
            xy=(row["mean_score"], row["range_score"]),
            xytext=offset,
            textcoords="offset points",
            fontsize=9,
            bbox=dict(
                boxstyle="round,pad=0.35",
                fc="white",
                ec="gray",
                alpha=0.95
            ),
            arrowprops=dict(
                arrowstyle="->",
                lw=1,
                color="gray"
            )
        )

    plt.tight_layout()

    # Save old filename so your project still works
    plt.savefig(output_dir / "mean_vs_disagreement.png", dpi=220)

    # Save clearer extra filename
    plt.savefig(output_dir / "mean_vs_disagreement_annotated.png", dpi=220)

    plt.close()