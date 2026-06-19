# LLMs - You Can't Please Them All: Real Judge Student Project

This is a VS Code-ready project for the Kaggle competition **LLMs - You Can't Please Them All**.

The project is designed for a Deep Learning course presentation. It uses an original pipeline:

1. Load Kaggle essay topics.
2. Generate multiple essay candidates per topic.
3. Score each candidate using a judge ensemble.
4. Select the essay that creates high disagreement while keeping a basic quality floor.
5. Export a Kaggle-style `submission.csv` and experiment files for your report.

The important upgrade from a purely biased/handmade judge is that this project can use a **real LLM judge**:

- `gemini`: uses Google Gemini API as the real judge.
- `ollama`: uses a local open-source LLM through Ollama.
- `heuristic`: no API baseline for debugging only.

---

## 1. Setup in VS Code

Open this folder in VS Code, then open the terminal.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

### Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

### Mac/Linux

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

---

## 2. Download Kaggle data

You have two options.

### Option A: Manual download

1. Go to Kaggle competition page.
2. Open the Data tab.
3. Download the dataset.
4. Put these files inside the `data/` folder:
   - `test.csv`
   - `sample_submission.csv` if available
   - `train.csv` if available

### Option B: Kaggle API

First, download `kaggle.json` from Kaggle Account Settings and place it in:

- Windows: `C:\Users\<YourName>\.kaggle\kaggle.json`
- Mac/Linux: `~/.kaggle/kaggle.json`

Then run:

```bash
python download_kaggle_data.py
```

You must accept the competition rules on Kaggle before the API can download the files.

---

## 3. First test run, no API key

```bash
python main.py --judge heuristic --max-topics 3
```

This creates:

```text
outputs/submission.csv
outputs/all_judge_scores.csv
outputs/candidate_summary.csv
outputs/selected_candidates.csv
outputs/run_summary.md
outputs/objective_distribution.png
outputs/mean_vs_disagreement.png
```

---

## 4. Use real judge with Gemini

Open `.env` and change:

```text
JUDGE_PROVIDER=gemini
GEMINI_API_KEY=paste_your_key_here
GEMINI_MODEL=gemini-1.5-flash
```

Then run:

```bash
python main.py --judge gemini --max-topics 3
```

When the first test works, run all topics:

```bash
python main.py --judge gemini
```

Notes:

- Real LLM judging costs API calls.
- Start with `--max-topics 3` to avoid wasting quota.
- The hidden Kaggle judge is not available locally, so this is an approximation for experimentation and presentation.

---

## 5. Use real local judge with Ollama

Install Ollama, then run:

```bash
ollama pull llama3.1:8b
```

Open `.env` and change:

```text
JUDGE_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b
OLLAMA_HOST=http://localhost:11434
```

Then run:

```bash
python main.py --judge ollama --max-topics 3
```

---

## 6. What to present

Use this structure in your slides:

1. **Problem**: LLM-as-a-judge systems may disagree when evaluating subjective essays.
2. **Dataset**: Kaggle provides essay topics and expects generated essays in the submission file.
3. **Baseline**: Generate one balanced academic essay for each topic.
4. **Proposed method**: Generate multiple candidate essays with different styles, then use a real LLM judge ensemble to score them.
5. **Selection objective**: Choose candidates with high judge disagreement while avoiding very low-quality essays.
6. **Experiments**:
   - Compare heuristic judge vs Gemini/Ollama judge.
   - Compare number of candidates: 3, 6, 8.
   - Compare strategies: academic, concise, creative, skeptical, structured.
7. **Results**: Show `candidate_summary.csv`, selected strategies, score range, and plots.
8. **Limitations**: Local/API judges do not exactly match Kaggle hidden judges; API cost; results can vary.

---

## 7. Academic integrity note

This project is meant as a modified, original implementation. If you used any public Kaggle notebook as inspiration, cite it clearly in your report and explain what you changed:

- Added real LLM judge option.
- Added multi-persona judge ensemble.
- Added disagreement-based candidate selection.
- Added experiment outputs and plots.
- Added reproducible VS Code project structure.

---

## 8. Folder structure

```text
llm_real_judge_project/
├── data/
├── docs/
├── experiments/
├── outputs/
├── src/
│   ├── config.py
│   ├── data.py
│   ├── essay_generator.py
│   ├── export.py
│   ├── judges.py
│   ├── selection.py
│   └── viz.py
├── .env.example
├── download_kaggle_data.py
├── main.py
├── README.md
├── requirements.txt
├── run_all.bat
└── run_all.sh
```
