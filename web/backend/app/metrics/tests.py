from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestMetricsEndpoint(APITestCase):
    def test_ok(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("get_radar_metrics")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [
            {"value": met, "label": met}
            for met in [
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
        self.assertEqual(response.json(), expected_response)
