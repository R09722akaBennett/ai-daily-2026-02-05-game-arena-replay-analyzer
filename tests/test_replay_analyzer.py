from fastapi.testclient import TestClient

from app.main import build_app


def test_analyze_detects_failures() -> None:
    client = TestClient(build_app())
    payload = {
        "steps": [
            {"t": 1, "action": "move", "reward": 0.0, "legal": True, "info": {}},
            {"t": 2, "action": "move", "reward": -1.0, "legal": False, "info": {}},
            {"t": 3, "action": "timeout", "reward": -2.0, "legal": True, "info": {}},
        ]
    }
    r = client.post("/api/v1/analyze", json=payload)
    assert r.status_code == 200
    analysis = r.json()["analysis"]
    assert analysis["failure_modes"].get("illegal_move", 0) >= 1
    assert analysis["failure_modes"].get("timeout", 0) >= 1


def test_compare_and_aggregate() -> None:
    client = TestClient(build_app())
    a = {"steps": [{"t": 1, "action": "move", "reward": 1.0, "legal": True, "info": {}}]}
    b = {"steps": [{"t": 1, "action": "move", "reward": 0.0, "legal": True, "info": {}}]}
    r = client.post("/api/v1/compare", json={"a": a, "b": b})
    assert r.status_code == 200
    assert "delta" in r.json()

    agg = client.post("/api/v1/aggregate", json={"matches": [a, b]})
    assert agg.status_code == 200
    assert agg.json()["summary"]["matches"] == 2
