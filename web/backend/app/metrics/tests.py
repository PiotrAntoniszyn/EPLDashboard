from django.urls import reverse
from metrics.fields import DEFAULT_RADAR_METRICS
from rest_framework import status
from rest_framework.test import APITestCase
from teams.tests import PlayerFactory


class TestMetricsEndpoint(APITestCase):
    def test_ok(self):
        url = reverse("get_radar_metrics")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [
            {"value": met, "label": met} for met in DEFAULT_RADAR_METRICS
        ]
        self.assertEqual(response.json(), expected_response)


class TestRadarChartEndpoint(APITestCase):
    @classmethod
    def setUpTestData(cls):
        PlayerFactory(id="1")

    def test_ok_no_metrics(self):
        url = reverse("get_radar_chart")
        response = self.client.get(url, data={"player_id": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            "metrics": [
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
            ],
            "name": "Edouard Mendy",
            "labels": [
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
            ],
        }
        self.assertEqual(response.json(), expected)

    def test_ok_selected_metrics(self):
        url = reverse("get_radar_chart")
        response = self.client.get(
            url, data={"player_id": 1, "metrics": ["Gls", "Ast"]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            "metrics": ["0", "0"],
            "name": "Edouard Mendy",
            "labels": ["Gls", "Ast"],
        }
        self.assertEqual(response.json(), expected)

    def test_invalid_metric_and_not_existing_player(self):
        url = reverse("get_radar_chart")
        response = self.client.get(url, data={"player_id": 2, "metrics": ["ABC"]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected = {
            "metrics": ["ABC is not a valid metric name"],
            "player_id": ["Player with id=2 does not exist"],
        }
        self.assertEqual(response.json(), expected)
