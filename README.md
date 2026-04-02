# LLM Judge Disagreement Project

## 📌 Problem Description
This project aims to generate essays that maximize disagreement among multiple LLM judges.

Different LLMs have different biases such as:
- Preference for formal vs informal writing
- Sensitivity to ethical issues
- Differences in logical reasoning

We exploit these biases by generating essays with:
- Contradictions
- Mixed writing styles
- Ambiguous arguments
- Ethical grey areas

---

## 📊 Dataset Overview
Dataset from Kaggle:
- Input: Essay topics
- Output: Generated essays

Example:
- "Discuss the role of self-reliance in software engineering"

---

## 📏 Evaluation Metric

We simulate LLM judges and compute:

- Average Quality Score
- Horizontal Standard Deviation (between judges)
- Vertical Standard Deviation (within essay)
- Engagement Score

Final Score Formula:

Higher disagreement (variance) = better score

---

## ⚙️ Pipeline

1. Load dataset (topics)
2. Generate essay using LLM (Gemma 2B/gpt-2)
3. Apply different writing strategies:
   - Philosophical
   - Metaphorical
   - Dialectical
4. Simulate multiple LLM judges
5. Compute disagreement score

---

## 📈 Baseline Performance

Example Result:
- Avg Quality: 3.87
- Disagreement Score: 22.94

Observation:
- Contradictory essays produce higher disagreement
- Ethical ambiguity increases variance

---

## 📁 Project Structure

- notebooks/ → EDA & model
- data/ → dataset explanation
- results/ → performance
- docs/ → methodology
