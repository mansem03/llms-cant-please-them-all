"""
LLM Judge Disagreement - IIUM Deep Learning Kaggle Track
VS Code / Python script version

Run:
    python llm_judge_disagreement_vscode.py
"""

import random
from pathlib import Path

import numpy as np
import pandas as pd


# -----------------------------
# 1. Enter your topics
# -----------------------------
topics = [
    "Compare the importance of self-reliance and adaptability in healthcare.",
    "Evaluate management consulting in addressing conflicts within marketing.",
    "Discuss the role of self-reliance in achieving success in software engineering.",
]


# -----------------------------
# 2. Essay generator
# -----------------------------
def generate_essay(topic):
    """Generate an intentionally ambiguous essay to create judge disagreement."""

    templates = [
        # Template 1 — philosophical / contradictory
        (
            "The question of {t} is, at its core, a paradox. "
            "Those who champion rigid principles claim they form the bedrock of progress — "
            "without them, systems collapse into chaos. "
            "Yet the same principles can become barriers when change demands flexibility. "
            "In this sense, the issue is both a solution and a problem, depending on who judges it."
        ),

        # Template 2 — metaphorical
        (
            "Think of {t} as a river and a dam. "
            "The river — wild and indifferent — represents raw potential. "
            "The dam channels it, makes it useful, but at a cost: the valley upstream drowns. "
            "Some may call this progress, while others may call it loss. "
            "Both views are reasonable, yet neither fully explains the whole situation."
        ),

        # Template 3 — dialectical / thesis-antithesis
        (
            "Thesis: {t} demands clarity, structure, and measurable outcomes. "
            "Antithesis: it demands empathy, ambiguity, and irreducible human judgment. "
            "Synthesis: neither alone is enough — yet combining them breeds its own contradictions. "
            "Practitioners who rely entirely on data risk missing what data was never designed to capture. "
            "However, those who reject data may also lose the discipline needed for fair judgment."
        ),
    ]

    chosen = random.choice(templates)
    return chosen.format(t=topic.lower().rstrip("."))


# -----------------------------
# 3. Scoring system
# -----------------------------
def score_essay(essay):
    """Simulate judge scores and calculate disagreement."""

    criteria = ["Introduction", "Logic", "Emotion", "Philosophy", "Conclusion"]
    judge_scores = {}

    for criterion in criteria:
        # 5 simulated judges each give a score from 0 to 10
        scores = [round(random.uniform(2, 10), 1) for _ in range(5)]
        judge_scores[criterion] = {
            "avg": round(np.mean(scores), 2),
            "stdev": round(np.std(scores), 2),
        }

    avgs = [v["avg"] for v in judge_scores.values()]
    stdevs = [v["stdev"] for v in judge_scores.values()]

    avg_quality = round(np.mean(avgs), 2)
    avg_disagreement = round(np.mean(stdevs), 2)
    min_disagreement = round(np.min(stdevs), 2)

    # Final score — higher means more disagreement between judges
    final_score = round(avg_disagreement * min_disagreement * (9 - avg_quality), 4)

    return judge_scores, avg_quality, avg_disagreement, final_score


# -----------------------------
# 4. Run experiment
# -----------------------------
def run_experiment():
    print(f"✅ You have {len(topics)} topic(s):")
    for i, topic in enumerate(topics, start=1):
        print(f"  {i}. {topic}")

    results = []

    for topic in topics:
        essay = generate_essay(topic)
        judge_data, avg_quality, avg_disagree, final_score = score_essay(essay)

        results.append({
            "topic": topic,
            "essay": essay,
            "judge_data": judge_data,
            "avg_quality": avg_quality,
            "avg_disagree": avg_disagree,
            "final_score": final_score,
        })

    print("\n✅ Done! Results:\n")

    for i, result in enumerate(results, start=1):
        print("=" * 60)
        print(f"Essay {i}: {result['topic']}")
        print("=" * 60)

        print("\n📄 ESSAY:")
        print(result["essay"])

        print("\n📊 JUDGE SCORES (avg ± disagreement):")
        for criterion, vals in result["judge_data"].items():
            bar = "█" * int(vals["avg"])
            print(f"  {criterion:<15} {bar:<10} avg={vals['avg']}  disagreement={vals['stdev']}")

        print(f"\n🎯 FINAL SCORE : {result['final_score']}")
        print(f"   Avg quality  : {result['avg_quality']} / 10")
        print(f"   Avg disagree : {result['avg_disagree']} (higher = judges disagree more)")
        print()

    # -----------------------------
    # 5. Summary table
    # -----------------------------
    summary_df = pd.DataFrame([{
        "Topic": r["topic"],
        "Avg Quality": r["avg_quality"],
        "Avg Disagree": r["avg_disagree"],
        "Final Score": r["final_score"],
    } for r in results])

    print("\n📌 SUMMARY TABLE:")
    print(summary_df.to_string(index=False))

    best_index = summary_df["Final Score"].idxmax()
    print(f"\n🏆 Best essay: Essay {best_index + 1}")
    print(f"   Topic: {results[best_index]['topic']}")
    print(f"   Score: {results[best_index]['final_score']}")

    # -----------------------------
    # 6. Save files
    # -----------------------------
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    submission = pd.DataFrame({
        "id": range(1, len(results) + 1),
        "essay": [r["essay"] for r in results],
    })

    full_results = pd.DataFrame([{
        "id": i + 1,
        "topic": r["topic"],
        "essay": r["essay"],
        "avg_quality": r["avg_quality"],
        "avg_disagree": r["avg_disagree"],
        "final_score": r["final_score"],
    } for i, r in enumerate(results)])

    submission.to_csv(output_dir / "submission.csv", index=False)
    full_results.to_csv(output_dir / "results.csv", index=False)

    print("\n✅ Files saved:")
    print("   outputs/submission.csv")
    print("   outputs/results.csv")


if __name__ == "__main__":
    run_experiment()
