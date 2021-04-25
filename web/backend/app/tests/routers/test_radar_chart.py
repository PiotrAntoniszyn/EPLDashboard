from typing import Tuple

from fastapi.testclient import TestClient

from app.main import app
from app.metrics.radar_chart import DEFAULT_RADAR_METRICS

client = TestClient(app)


def test_getting_metrics():
    response = client.get("/radar/metrics")
    assert response.status_code == 200
    expected_metrics = [
        {"value": name, "label": name} for name in DEFAULT_RADAR_METRICS
    ]
    assert response.json(), expected_metrics


def test_get_radar_chart_ok_no_metrics():
    response = client.get("/radar", params={"player_id": 1})
    assert response.status_code == 200

    data = response.json()
    assert data["labels"], DEFAULT_RADAR_METRICS
    assert data["name"], "Mason Mount"
    expected_metrics = [
        "0",
        "0",
        "0",
        "0",
        "0",
        "1",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
    ]
    assert data["metrics"], expected_metrics


def test_get_radar_chart_ok_with_metrics():
    response = client.get(
        "/radar", params={"player_id": 1, "metrics": DEFAULT_RADAR_METRICS[:2]}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["labels"], DEFAULT_RADAR_METRICS[:2]
    assert data["name"], "Mason Mount"

    expected_metrics = ["0", "0"]
    assert data["metrics"], expected_metrics


def test_get_radar_chart_invalid_player_id():
    response = client.get("/radar", params={"player_id": 100})
    assert response.status_code == 404
    assert response.json()["detail"], "Player not found"


def test_get_radar_chart_invalid_metric_passes():
    response = client.get(
        "/radar", params={"player_id": 1, "metrics": "non_existing_metric"}
    )
    assert response.status_code == 404
    assert response.json()["detail"], "Invalid metric requested"
