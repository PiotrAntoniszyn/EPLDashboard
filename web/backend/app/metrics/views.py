import json

from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def get_radar_metrics(_):
    DEFAULT_RADAR_METRICS = [
        "Gls",
        "Ast",
        "G-PK",
        "PK",
        "PKatt",
        "CrdY",
        "CrdR",
        "Gls__1",
        "Ast__1",
        "G+A",
        "G-PK__1",
        "G+A-PK",
        "xG",
        "npxG",
        "xA",
        "npxG+xA",
        "xG__1",
        "xA__1",
        "xG+xA",
        "npxG__1",
        "npxG+xA__1",
    ]
    return Response([{"value": met, "label": met} for met in DEFAULT_RADAR_METRICS])


@api_view(["GET"])
def get_radar_chart(_, player_id):
    with open("metrics/fixtures/radar_chelsea.json", "r") as f:
        data = json.loads(f.read())

    try:
        player_data = data[player_id]
    except IndexError:
        return Response(status_code=404, detail="Player not found")

    player_name = player_data["Player"].split("\\")[0]
    # if not metrics:
    metrics = [
        d for d in 
        [
            "Gls",
            "Ast",
            "G-PK",
            "PK",
            "PKatt",
            "CrdY",
            "CrdR",
            "Gls__1",
            "Ast__1",
            "G+A",
            "G-PK__1",
            "G+A-PK",
            "xG",
            "npxG",
            "xA",
            "npxG+xA",
            "xG__1",
            "xA__1",
            "xG+xA",
            "npxG__1",
            "npxG+xA__1",
        ]
    ]

    try:
        player_metrics = [player_data[column] for column in metrics]
    except KeyError:
        return Response(status_code=404, detail="Invalid metric requested")

    return Response({"metrics": player_metrics, "name": player_name, "labels": metrics})