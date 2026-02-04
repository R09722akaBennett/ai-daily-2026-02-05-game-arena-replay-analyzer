# Game Arena Replay Analyzer
Slug: game-arena-replay-analyzer

## Problem
Interactive game/arena benchmarks produce win/loss but limited insight. A replay analyzer converts trajectories into a compact error taxonomy + swing moments + comparisons.

## Users
- Kaggle/Game Arena competitors
- Researchers evaluating sequential decision agents

## MVP
- Ingest replays/trajectories (JSON/NDJSON) in a simple schema
- Produce per-match analysis.json + analysis.md
- Aggregate summary across a folder
- Compare two runs and show deltas

## Non-goals
- Not a simulator
- Not training

## API
- `POST /v1/analyze`
- `POST /v1/aggregate`
- `POST /v1/compare`

## UI
- Streamlit: upload replays, view timeline and top swing moments

## Acceptance criteria
- Detect at least 5 failure modes with unit tests
- Aggregation works

## Risks
- Replay format variability; mitigate with adapters + strict core schema

## Sources
- https://blog.google/innovation-and-ai/models-and-research/google-deepmind/kaggle-game-arena-updates/
