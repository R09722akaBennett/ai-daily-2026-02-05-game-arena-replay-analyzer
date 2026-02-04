from __future__ import annotations

import json
import os

import httpx
import streamlit as st

API_URL = os.getenv("UI_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Replay Analyzer", layout="centered")
st.title("Game Arena Replay Analyzer")
st.caption("Analyze a simple trajectory: failure modes + top swing moments.")

sample = {
    "steps": [
        {"t": 1, "action": "move", "reward": 0.0, "legal": True},
        {"t": 2, "action": "move", "reward": -1.0, "legal": False},
        {"t": 3, "action": "noop", "reward": 0.0, "legal": True},
        {"t": 4, "action": "timeout", "reward": -2.0, "legal": True},
    ]
}

text = st.text_area("Trajectory JSON", value=json.dumps(sample, indent=2), height=220)

if st.button("Analyze", type="primary"):
    payload = json.loads(text)
    with httpx.Client(base_url=API_URL, timeout=10.0) as client:
        r = client.post("/api/v1/analyze", json=payload)
        st.json(r.json())

st.caption(f"API: {API_URL}")
