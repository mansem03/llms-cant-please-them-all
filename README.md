# LLM Judge Disagreement Project

## Project Overview

This repository documents a progressive deep learning / NLP coursework project inspired by the Kaggle competition **LLMs - You Can't Please Them All**.

The main objective is to generate essays that create disagreement among multiple Large Language Model (LLM) judges. Instead of optimizing only for a single quality score, this project explores how different essay styles, judge preferences, and evaluation strategies can produce different scoring outcomes.

The project is organized into **Assessment 1, Assessment 2, and Assessment 3**, showing the development from a simple simulated judge pipeline to a more advanced real-LLM judge workflow.

---

## Problem Description

LLM judges may not always agree when evaluating the same essay. Different judges may prefer different qualities such as:

- formal academic writing
- emotional and persuasive language
- logical structure
- philosophical or abstract reasoning
- ethical sensitivity
- concise and direct answers

This project attempts to exploit these differences by generating essays with:

- contradictory arguments
- mixed writing styles
- ethical ambiguity
- abstract and philosophical ideas
- emotional and metaphorical language
- structured and unstructured reasoning patterns

The central research question is:

> How can essay generation strategies be designed to increase disagreement among multiple LLM judges while keeping the essay relevant to the given topic?

---

## Dataset Overview

The project uses Kaggle-style essay topics.

Expected input format:

```csv
id,topic
1,Compare the importance of self-reliance and adaptability in healthcare.
```

Expected output format:

```csv
id,essay
1,Generated essay text here
```

Example topics used in this project include:

- Compare the importance of self-reliance and adaptability in healthcare.
- Evaluate management consulting in addressing conflicts within marketing.
- Discuss the role of self-reliance in achieving success in software engineering.

---

## Assessment 1: Baseline LLM Judge Disagreement

Assessment 1 implements a local Python pipeline using template-based essay generation.

### Main Features

- Defines a small list of essay topics.
- Generates essays using ambiguous writing templates.
- Uses philosophical, metaphorical, and dialectical essay styles.
- Simulates multiple judge scores.
- Calculates average quality, disagreement, and final score.
- Exports results to CSV files.

### Essay Generation Styles

- Philosophical / contradictory
- Metaphorical
- Dialectical / thesis-antithesis-synthesis

### Assessment 1 Output Files

```text
Assessment_1/
├── assessment1_llm.py
└── outputs/
    ├── results.csv
    └── submission.csv
```

---

## Assessment 2: Gemini-Based Adversarial Essay Generation

Assessment 2 improves the baseline by using Gemini as the essay generation model.

### Main Features

- Uses Google Gemini API for essay generation.
- Applies adversarial prompt strategies.
- Simulates a judge committee with different evaluation biases.
- Calculates pairwise judge differences.
- Computes maximum gap, variance, quality score, and final system score.

### Adversarial Strategies

1. **The Contradictor**  
   Generates essays that argue two opposite points at once.

2. **The Jargon-Bomb**  
   Uses dense academic vocabulary to increase perceived sophistication while reducing readability.

3. **The Emotional-Hook**  
   Uses dramatic metaphors and emotional intensity to create subjective interpretation differences.

### Judge Simulation

Assessment 2 uses three judge personas:

- J1: strict and grammar-focused
- J2: emotion-sensitive
- J3: logical and structured

### Evaluation Criteria

- Grammar & Vocabulary
- Coherence
- Development
- Content
- Emotion

### Final Score Formula

```text
final_score = average_variance × (9 - average_quality)
```

A higher final score indicates stronger disagreement among the judge committee.

---

## Assessment 3: Real LLM Judge Ensemble

Assessment 3 extends the project into a more complete real-judge experiment pipeline.

### Main Features

- Generates multiple candidate essays per topic.
- Uses several prompt styles for candidate generation.
- Applies real or external LLM judge personas.
- Tracks candidate scores, disagreement, range, and word count.
- Selects the best essay based on an objective score.
- Produces reproducible output files for analysis and submission.

### Candidate Styles

- academic balanced
- creative reflective
- concise direct
- skeptical logic
- pro/con contrast
- structured headings
- empathetic social
- uncertainty aware

### Assessment 3 Output Files

Expected output files include:

```text
outputs/candidate_summary.csv
outputs/selected_candidates.csv
outputs/all_judge_scores.csv
outputs/objective_distribution.png
outputs/mean_vs_disagreement.png
outputs/submission.csv
```

---

## Evaluation Metric

The evaluation focuses on disagreement between multiple judges.

The project computes several metrics:

- **Average Quality Score**  
  Measures the general quality of the essay across judges.

- **Standard Deviation / Variance**  
  Measures disagreement between judge scores.

- **Score Range / Maximum Gap**  
  Measures the difference between the highest and lowest judge scores.

- **Pairwise Judge Differences**  
  Shows which judges disagree the most.

- **Objective Score**  
  Combines quality and disagreement to select the best candidate essay.

Higher disagreement means the same essay is interpreted differently by different judges.

---

## Overall Pipeline

```text
1. Load essay topics
2. Generate candidate essays
3. Apply different writing strategies
4. Evaluate essays using simulated or real LLM judges
5. Compute quality and disagreement metrics
6. Select the best essay for each topic
7. Export submission and result files
8. Analyze performance and limitations
```

---

## Key Observations

- Contradictory essays can increase disagreement because judges may disagree on coherence and logic.
- Emotional essays can create high disagreement because emotion is subjective.
- Dense academic language may score highly for vocabulary but poorly for clarity.
- A high-quality essay does not always maximize disagreement.
- Real LLM judges provide a more realistic evaluation than handcrafted scoring rules.
- The hidden Kaggle judge cannot be perfectly reproduced locally, so local evaluation is an approximation.

---

## Project Structure

```text
llms-cant-please-them-all/
│
├── README.md
│
├── Assessment_1/
│   ├── assessment1_llm.py
│   └── outputs/
│       ├── results.csv
│       └── submission.csv
│
├── Assessment_2/
│   ├── ASSESSMENT2_CODE.py
│   ├── REPORT_Assesment2_GROUPAFIQQ.pdf
│   └── outputs/
│
├── Assessment_3/
│   ├── report_assessment3.pdf
│   ├── report_assessment3.docx
│   ├── project_code/
│   └── outputs/
│       ├── candidate_summary.csv
│       ├── selected_candidates.csv
│       ├── all_judge_scores.csv
│       └── submission.csv
│
├── dataset_description.md
├── methodology.md
└── slidesLLM_Judge_Presentation.pdf
```

---

## How to Run

### Assessment 1

```bash
cd Assessment_1
pip install numpy pandas
python assessment1_llm.py
```

### Assessment 2

```bash
cd Assessment_2
pip install numpy pandas google-genai
python ASSESSMENT2_CODE.py
```

Before running Assessment 2, set your Gemini API key securely using an environment variable. Do not upload API keys directly to GitHub.

### Assessment 3

```bash
cd Assessment_3
pip install -r requirements.txt
python main.py
```

The exact command may differ depending on the final Assessment 3 project file name.

---

## Security Note

Do not commit private API keys, `.env` files, or credentials to GitHub.

If an API key was accidentally committed, remove it from the code, revoke the old key, and create a new key.

Recommended format:

```python
import os
api_key = os.getenv("GEMINI_API_KEY")
```

---

## Limitations

- Assessment 1 uses simulated scoring, so the judge behavior is not fully realistic.
- Assessment 2 uses a real generator but still uses simulated judge biases.
- Assessment 3 improves the workflow by introducing a real-judge ensemble, but it still cannot perfectly reproduce Kaggle's hidden evaluation.
- Results may vary due to randomness, prompt sensitivity, and model updates.
- API-based experiments may require internet access and may involve cost.

---

## Conclusion

This project demonstrates a full progression of an LLM judge disagreement system. Assessment 1 establishes a baseline pipeline, Assessment 2 introduces real LLM-based essay generation with adversarial strategies, and Assessment 3 expands the work into a more complete real-judge ensemble framework.

Overall, the project shows that essay evaluation is subjective and that different judge personas can produce different interpretations of the same generated text. This supports the main idea of the Kaggle competition: **you cannot please every LLM judge at the same time**.
