# Project Report Template

## Title
Real LLM Judge Ensemble for Adversarial Essay Generation in Kaggle LLMs - You Can't Please Them All

## 1. Introduction
This project studies the robustness of LLM-as-a-judge systems. In subjective writing tasks, different judges may prefer different writing styles. The goal is to generate essays that create disagreement among judges while remaining relevant to the topic.

## 2. Problem Understanding
The Kaggle competition provides essay topics. A submission contains an essay for each topic. The hidden evaluation uses multiple LLM judges. A higher score is related to the ability to produce essays that lead to judge disagreement.

## 3. Baseline
The baseline method generates one balanced academic essay for each topic using a fixed template. It is simple, reproducible, and easy to explain, but it may not create much disagreement.

## 4. Proposed Method
The proposed method generates several candidate essays for each topic using different styles:

- academic balanced
- creative reflective
- concise direct
- skeptical logic
- pro/con contrast
- structured headings
- empathetic social
- uncertainty aware

Each candidate is scored by several judge personas. In the improved version, the personas are implemented using a real LLM judge through Gemini or Ollama.

## 5. Selection Objective
For each candidate, the system calculates:

- mean score
- standard deviation of judge scores
- score range
- word count
- objective score

The selected essay maximizes judge disagreement while avoiding very low mean score and unsuitable essay length.

## 6. Experiments
Suggested experiments:

| Experiment | Judge | Candidates per topic | Purpose |
|---|---|---:|---|
| E1 | heuristic | 3 | Debug baseline pipeline |
| E2 | heuristic | 6 | Check effect of more candidates |
| E3 | Gemini | 3 | Test real judge output |
| E4 | Gemini | 6 | Compare real judge disagreement |
| E5 | Ollama | 6 | Compare local LLM judge |

## 7. Results and Analysis
Use the generated files:

- `outputs/candidate_summary.csv`
- `outputs/selected_candidates.csv`
- `outputs/all_judge_scores.csv`
- `outputs/objective_distribution.png`
- `outputs/mean_vs_disagreement.png`

Discuss which strategy was selected most often and whether the real judge produced larger or smaller disagreement compared with the heuristic judge.

## 8. Limitations
The hidden Kaggle judge is not available locally. Gemini/Ollama are only approximations. Scores may change due to randomness and model updates. API usage may also cost money, so experiments should start with a small number of topics.

## 9. Conclusion
The project demonstrates a complete deep learning/NLP workflow: topic processing, LLM-based judging, candidate generation, experiment tracking, selection objective design, and reproducible submission export. The real-judge version improves over a biased manual judge because it uses actual LLM evaluation instead of only handcrafted rules.
