import factory
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from teams.models import Player

class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player


class TestGetPlayersEndpoint(APITestCase):

    def test_ok(self):
        PlayerFactory(first_name="Timo", last_name="Verner", age=20, position="Goalkeeper")
        url = reverse('get_players')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{ "label": "Timo Verner", "value": 1}])
