from datetime import datetime
from transport import Bus, Tram
from route import Route, Segment
from trip import Trip
from statistics import Stats


def create_routes():
    route1 = Route("Route No.1")
    route1.add_segment(Segment("Centrum → Rynek",
                                traffic_level=8, rail_condition=5, has_tram_lane=False))
    route1.add_segment(Segment("Rynek → Plac Wolnosci",
                                traffic_level=6, rail_condition=6, has_tram_lane=False))
    route1.add_segment(Segment("Plac Wolnosci → Dworzec Glowny",
                                traffic_level=4, rail_condition=7, has_tram_lane=False))

    # Route 2 — Bus route (Dworzec → Osiedle)
    route2 = Route("Route No.2")
    route2.add_segment(Segment("Dworzec Glowny → Politechnika",
                                traffic_level=5, rail_condition=8, has_tram_lane=False))
    route2.add_segment(Segment("Politechnika → Osiedle Kowalskiego",
                                traffic_level=3, rail_condition=9, has_tram_lane=False))

    # Route 3 — Tram route (Centrum → Park)
    route3 = Route("Route No.3")
    route3.add_segment(Segment("Centrum → Uniwersytet",
                                traffic_level=7, rail_condition=4, has_tram_lane=True))
    route3.add_segment(Segment("Uniwersytet → Muzeum Narodowe",
                                traffic_level=5, rail_condition=6, has_tram_lane=False))
    route3.add_segment(Segment("Muzeum Narodowe → Park Miejski",
                                traffic_level=2, rail_condition=8, has_tram_lane=True))

    # Route 4 — Tram route (Dworzec → Stadion)
    route4 = Route("Route No.4")
    route4.add_segment(Segment("Dworzec Glowny → Plac Konstytucji",
                                traffic_level=6, rail_condition=3, has_tram_lane=False))
    route4.add_segment(Segment("Plac Konstytucji → Aleje Jerozolimskie",
                                traffic_level=8, rail_condition=5, has_tram_lane=True))
    route4.add_segment(Segment("Aleje Jerozolimskie → Stadion Miejski",
                                traffic_level=4, rail_condition=7, has_tram_lane=True))

    return route1, route2, route3, route4


def create_transport():
    bus1 = Bus("A101")
    bus2 = Bus("A202")
    tram1 = Tram("T3")
    tram2 = Tram("T5")
    return bus1, bus2, tram1, tram2


def simulate_day(route1, route2, route3, route4, bus1, bus2, tram1, tram2):
    stats = Stats()

    # Morning rush hour 08:00 - 09:00
    stats.add_trip(Trip(bus1, route1,
                        datetime(2024, 1, 1, 8, 0),
                        datetime(2024, 1, 1, 8, 16)))
    stats.add_trip(Trip(bus2, route2,
                        datetime(2024, 1, 1, 8, 15),
                        datetime(2024, 1, 1, 8, 25)))
    stats.add_trip(Trip(tram1, route3,
                        datetime(2024, 1, 1, 8, 30),
                        datetime(2024, 1, 1, 8, 55)))
    stats.add_trip(Trip(tram2, route4,
                        datetime(2024, 1, 1, 8, 45),
                        datetime(2024, 1, 1, 9, 15)))

    # Daytime 13:00 - 14:00
    stats.add_trip(Trip(bus1, route2,
                        datetime(2024, 1, 1, 13, 0),
                        datetime(2024, 1, 1, 13, 8)))
    stats.add_trip(Trip(tram1, route4,
                        datetime(2024, 1, 1, 13, 20),
                        datetime(2024, 1, 1, 13, 35)))
    stats.add_trip(Trip(bus2, route1,
                        datetime(2024, 1, 1, 13, 45),
                        datetime(2024, 1, 1, 13, 50)))

    # Evening rush hour 17:00 - 19:00
    stats.add_trip(Trip(bus1, route1,
                        datetime(2024, 1, 1, 17, 0),
                        datetime(2024, 1, 1, 17, 20)))
    stats.add_trip(Trip(tram2, route3,
                        datetime(2024, 1, 1, 17, 15),
                        datetime(2024, 1, 1, 17, 45)))
    stats.add_trip(Trip(bus2, route2,
                        datetime(2024, 1, 1, 18, 0),
                        datetime(2024, 1, 1, 18, 12)))
    stats.add_trip(Trip(tram1, route4,
                        datetime(2024, 1, 1, 18, 30),
                        datetime(2024, 1, 1, 19, 5)))

    return stats


def print_report(stats):
    print("=" * 60)
    print("    CITY TRANSPORT MONITOR — DAILY REPORT")
    print("=" * 60)

    # Группируем рейсы по маршрутам
    routes_trips = {}
    for trip in stats.trips:
        route_name = trip.route.name
        if route_name not in routes_trips:
            routes_trips[route_name] = trip.route, []
        routes_trips[route_name][1].append(trip)

    # Выводим по каждому маршруту
    for route_name, (route, trips) in routes_trips.items():
        print(f"\n--- {route_name} ---")

        print("  Segments:")
        for s in route.segments:
            print(f"    {s.name:<40} | "
                  f"Traffic: {s.traffic_level}/10 | "
                  f"Rail: {s.rail_condition}/10 | "
                  f"Tram lane: {'yes' if s.has_tram_lane else 'no'}")

        print("  Trips:")
        for trip in trips:
            print(f"    {trip.vehicle.get_info()} | "
                  f"Schedule: {trip.scheduled_time.strftime('%H:%M')} | "
                  f"Actual: {trip.actual_time.strftime('%H:%M')} | "
                  f"Delay: {trip.get_delay()} | "
                  f"Passengers: {trip.get_percent()}%")

    print("\n" + "=" * 60)
    print("  STATISTICS:")
    print(f"  Total trips:        {len(stats.trips)}")
    print(f"  Average delay:      {stats.average_delay()}")
    print(f"  Busiest route:      {stats.busiest_route()}")

    print("\n  PASSENGERS BY TIME PERIOD:")
    print(f"  Morning (08:00-10:00): "
          f"{stats.total_passengers(datetime(2024, 1, 1, 8, 0), datetime(2024, 1, 1, 10, 0))} passengers")
    print(f"  Daytime (13:00-14:00): "
          f"{stats.total_passengers(datetime(2024, 1, 1, 13, 0), datetime(2024, 1, 1, 14, 0))} passengers")
    print(f"  Evening (17:00-19:00): "
          f"{stats.total_passengers(datetime(2024, 1, 1, 17, 0), datetime(2024, 1, 1, 19, 0))} passengers")
    print("=" * 60)


if __name__ == "__main__":
    route1, route2, route3, route4 = create_routes()
    bus1, bus2, tram1, tram2 = create_transport()
    stats = simulate_day(route1, route2, route3, route4, bus1, bus2, tram1, tram2)
    print_report(stats)