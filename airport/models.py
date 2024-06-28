from django.db import models
from django.conf import settings


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey("AirplaneType",
                                      on_delete=models.CASCADE,
                                      related_name="airplanes")


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closet_big_city = models.ForeignKey(City, on_delete=models.CASCADE)


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE)
    distance = models.IntegerField()


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
