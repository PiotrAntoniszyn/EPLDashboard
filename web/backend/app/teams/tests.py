from django.urls import reverse
from factory import fuzzy
from factory.django import DjangoModelFactory
from rest_framework import status
from rest_framework.test import APITestCase
from teams.models import Player, Team


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    first_name = fuzzy.FuzzyChoice(["Timo", "Bob", "Andrew"])
    last_name = fuzzy.FuzzyChoice(["Verner", "Hawk", "Stark"])
    age = fuzzy.FuzzyInteger(18, 40)
    position = fuzzy.FuzzyChoice(["Goalkeeper", "Defence"])


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = fuzzy.FuzzyText()


class TestGetPlayersEndpoint(APITestCase):
    def test_ok(self):
        PlayerFactory(
            first_name="Timo", last_name="Verner", age=20, position="Goalkeeper"
        )
        url = reverse("get_players")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{"label": "Timo Verner", "value": 1}])


class TestGetPlayerByIdEndpoint(APITestCase):
    def test_ok(self):
        team = TeamFactory()
        player = PlayerFactory(id=1, team=team)
        url = reverse("get_player_by_id", kwargs={"player_id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "first_name": player.first_name,
                "last_name": player.last_name,
                "score": player.score,
                "age": player.age,
                "team_name": player.team.name,
            },
        )

    def test_not_existing_player(self):
        url = reverse("get_player_by_id", kwargs={"player_id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {"player_id": [["Cannot find player with id 1"]]}
        )
