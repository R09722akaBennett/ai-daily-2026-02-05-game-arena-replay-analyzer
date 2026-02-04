# Game Arena Replay Analyzer

Tiny daily AI-trend microproject (FastAPI + Streamlit) — generated on 2026-02-05.

## Why
Interactive benchmarks (games/arenas) are a richer signal for agents than static QA, but debugging is hard. This project turns a replay into failure mode counts and swing moments.

## What it does
- FastAPI backend (`/api/*`)
- Streamlit UI (`app/web/streamlit_app.py`)
- Minimal unit tests (pytest)

## Run locally
```bash
python -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -e .

# API
uvicorn app.main:build_app --factory --host 0.0.0.0 --port 8000

# UI (in another shell)
streamlit run app/web/streamlit_app.py
```

## Sources
- https://blog.google/innovation-and-ai/models-and-research/google-deepmind/kaggle-game-arena-updates/

## Roadmap
- Add adapters for specific replay formats\n- Add richer swing detection (win-prob proxies)\n- Add a timeline web viewer
