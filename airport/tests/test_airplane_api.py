from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airplane, AirplaneType
from airport.serializers import AirplaneListSerializer, AirplaneDetailSerializer
from airport.tests.sample_data import sample_airplane


AIRPLANE_URL = reverse("airport:airplane-list")


def detail_url(airplane_id):
    return reverse("airport:airplane-detail", args=[airplane_id])


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_filter_airplanes_by_airplane_types(self):
        airplane_type1 = AirplaneType.objects.create(name="Airplane type 1")
        airplane_type2 = AirplaneType.objects.create(name="Airplane type 2")
        airplane_type3 = AirplaneType.objects.create(name="Airplane type 3")

        airplane1 = sample_airplane(name="Airplane 1", airplane_type=airplane_type1)
        airplane2 = sample_airplane(name="Airplane 2", airplane_type=airplane_type2)
        airplane3 = sample_airplane(name="Airplane 3", airplane_type=airplane_type3)

        res = self.client.get(
            AIRPLANE_URL,
            {"airplane_types": f"{airplane_type1.id}, {airplane_type2.id}"},
        )

        serializer1 = AirplaneListSerializer(airplane1)
        serializer2 = AirplaneListSerializer(airplane2)
        serializer3 = AirplaneListSerializer(airplane3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_airplane_detail(self):
        airplane = sample_airplane()

        url = detail_url(airplane.id)
        res = self.client.get(url)

        serializer = AirplaneDetailSerializer(airplane)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airplane_forbidden(self):
        airplane_type = AirplaneType.objects.create(name="Boeing 747")

        payload = {
            "name": "Forbidden Airplane",
            "rows": 20,
            "seats_in_row": 4,
            "airplane_type": airplane_type.pk,
        }

        res = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane(self):
        airplane_type = AirplaneType.objects.create(name="Boeing 747")

        payload = {
            "name": "Forbidden Airplane",
            "rows": 20,
            "seats_in_row": 4,
            "airplane_type": airplane_type.pk,
        }

        res = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
