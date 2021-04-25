import json
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Query

from app.metrics.radar_chart import DEFAULT_RADAR_METRICS

router = APIRouter(tags=["Radar chart"])


@router.get("/radar")
def get_radar_chart(player_id: int, metrics: List[str] = Query(None)) -> Dict:
    with open("app/fixtures/radar_chelsea.json", "r") as f:
        data = json.loads(f.read())

    try:
        player_data = data[player_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Player not found")

    player_name = player_data["Player"].split("\\")[0]
    if not metrics:
        metrics = [d["value"] for d in get_radar_metrics()]

    try:
        player_metrics = [player_data[column] for column in metrics]
    except KeyError:
        raise HTTPException(status_code=404, detail="Invalid metric requested")

    return {"metrics": player_metrics, "name": player_name, "labels": metrics}


@router.get("/radar/metrics")
def get_radar_metrics() -> List[Dict]:
    return [{"value": name, "label": name} for name in DEFAULT_RADAR_METRICS]
