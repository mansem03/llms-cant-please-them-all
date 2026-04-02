# LLM Judge Disagreement Project

## 📌 Problem Description
This project is based on a Kaggle competition where the goal is to generate essays that maximize disagreement between multiple LLM judges.

## 📊 Dataset Overview
The dataset consists of:
- Essay topics
- Generated essays
- Scores from multiple LLM judges

## 📏 Evaluation Metric
We use disagreement score (standard deviation of scores).

- Low variance → judges agree
- High variance → judges disagree (better)

## ⚙️ Pipeline
1. Select topic
2. Generate essay
3. Evaluate using multiple judges
4. Compute disagreement score

## 📈 Baseline Result
Baseline Score: 

## 📁 Project Structure
- notebooks/ → EDA & model
- data/ → dataset explanation
- results/ → performance
- docs/ → methodology
