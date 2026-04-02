# LLM Judge Disagreement Project

## 📌 Problem Description
This project aims to generate essays that maximize disagreement among multiple Large Language Model (LLM) judges.

Different LLMs have different biases such as:
- Preference for formal vs informal writing
- Sensitivity to ethical arguments
- Differences in logical reasoning

This project exploits these biases by generating essays with:
- Contradictory arguments
- Mixed writing styles
- Ethical ambiguity
- Abstract and philosophical ideas

---

## 📊 Dataset Overview
The dataset consists of essay topics from a Kaggle competition.

Each topic is used to generate an essay using a language model.

Example:
- "Discuss the role of self-reliance in achieving success in software engineering"

---

## 📏 Evaluation Metric
The evaluation is based on disagreement between multiple LLM judges.

We compute:
- Average Quality Score
- Horizontal Standard Deviation (difference between judges)
- Vertical Standard Deviation (variation across sections)
- Engagement Score

Higher disagreement (variance) = better performance.

---

## ⚙️ Pipeline
1. Load dataset (topics)
2. Generate essay using LLM
3. Apply different writing styles:
   - Philosophical
   - Metaphorical
   - Dialectical
4. Simulate multiple LLM judges
5. Compute disagreement score

---

## 📈 Baseline Results
Example scores:

- Essay 1: 22.94  
- Essay 2: 11.34  
- Essay 3: 7.58  

### Key Observations:
- Contradictory essays increase disagreement
- Ethical ambiguity confuses LLM judges
- Mixed writing styles produce higher variance

---

## 📁 Project Structure
- notebooks/ → EDA and model notebooks
- data/ → dataset description
- results/ → performance results
- docs/ → methodology explanation

---

## ⚠️ Note
LLM judges are simulated using random scoring for baseline purposes. Future work can include real LLM evaluation.
