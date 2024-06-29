from django.db import models
from django.conf import settings


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        "AirplaneType", on_delete=models.CASCADE, related_name="airplanes"
    )

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"Country: {self.country}, City: {self.name}"


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closet_big_city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.closet_big_city})"


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="sources_route"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destinations_route"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created_at} - {self.user}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        "Flight", on_delete=models.CASCADE, related_name="flights"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order: {self.order} (row: {self.row}, seat: {self.seat})"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="routes")
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="airplanes"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name="crews")

    def __str__(self):
        return self.route
