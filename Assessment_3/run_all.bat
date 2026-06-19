@echo off
REM Windows helper script
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
python main.py --judge heuristic --max-topics 3
pause
