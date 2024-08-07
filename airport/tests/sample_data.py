from airport.models import (
    Airplane,
    AirplaneType,
    Country,
    City,
    Airport,
    Route,
    Crew,
    Flight,
)


def sample_airplane(**params):
    airplane_type = AirplaneType.objects.create(name="Boeing 747")

    defaults = {
        "name": "Skyliner X",
        "rows": 20,
        "seats_in_row": 4,
        "airplane_type": airplane_type,
    }
    defaults.update(params)

    return Airplane.objects.create(**defaults)


def sample_city(**params):
    country = Country.objects.create(name="France")

    defaults = {"name": "Paris", "country": country}
    defaults.update(params)

    return City.objects.create(**defaults)


def sample_airport(**params):
    city = sample_city()

    defaults = {"name": "Charles de Gaulle Airport", "closest_big_city": city}
    defaults.update(params)

    return Airport.objects.create(**defaults)


def sample_route(**params):
    source = sample_airport(name="Source Airport")
    destination = sample_airport(name="Destination Airport")

    defaults = {"source": source, "destination": destination, "distance": 3458}
    defaults.update(params)

    return Route.objects.create(**defaults)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()
    crew = Crew.objects.create(first_name="FirstName", last_name="LastName")

    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": "2023-11-18T14:00:00+02:00",
        "arrival_time": "2023-11-18T19:00:00+02:00",
    }
    defaults.update(params)

    flight = Flight.objects.create(**defaults)
    flight.crew.add(crew)
    flight.tickets_available = 80

    return flight
