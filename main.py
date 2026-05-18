from datetime import datetime, timedelta
from transport import Bus, Tram
from route import Route, Segment
from trip import Trip
from statistics import Stats
from city_data import get_city_routes, get_city_vehicles


def create_route():
    name = input("Route name: ")
    route = Route(name)

    while True:
        print("\n  1. Add segment")
        print("  2. Finish route")
        choice = input("  Choice: ")

        if choice == "1":
            seg_name = input("  Segment name (e.g. Centrum → Rynek): ")
            while True:
                try:
                    traffic = int(input("  Traffic level (1-10): "))
                    rail = int(input("  Rail condition (1-10): "))
                    break
                except ValueError:
                    print("  Please enter a number!")
            tram_lane = input("  Tram lane? (yes/no): ").strip().lower() == "yes"
            route.add_segment(Segment(seg_name, traffic_level=traffic,
                                      rail_condition=rail, has_tram_lane=tram_lane))
            print(f"  Segment '{seg_name}' added!")

        elif choice == "2":
            if not route.segments:
                print("  Route must have at least one segment!")
            else:
                break

    return route


def create_trip(routes):
    if not routes:
        print("No routes available! Create a route first.")
        return None

    print("\nAvailable routes:")
    for i, route in enumerate(routes):
        print(f"  {i + 1}. {route.name}")

    while True:
        try:
            route_index = int(input("Choose route number: ")) - 1
            if 0 <= route_index < len(routes):
                break
            print("Invalid number!")
        except ValueError:
            print("Please enter a number!")

    route = routes[route_index]
    transport_type = input("Transport type (bus/tram): ").strip().lower()
    number = input("Vehicle number (e.g. A101): ").strip()
    vehicle = Bus(number) if transport_type == "bus" else Tram(number)

    while True:
        try:
            scheduled = input("Scheduled time (HH:MM): ").strip()
            actual = input("Actual time (HH:MM): ").strip()
            scheduled_time = datetime.strptime(f"2024-01-01 {scheduled}", "%Y-%m-%d %H:%M")
            actual_time = datetime.strptime(f"2024-01-01 {actual}", "%Y-%m-%d %H:%M")
            break
        except ValueError:
            print("Invalid time format! Use HH:MM")

    return Trip(vehicle, route, scheduled_time, actual_time)


def show_statistics(stats):
    if not stats.trips:
        print("No trips yet!")
        return

    routes_trips = {}
    for trip in stats.trips:
        route_name = trip.route.name
        if route_name not in routes_trips:
            routes_trips[route_name] = (trip.route, [])
        routes_trips[route_name][1].append(trip)

    print("\n" + "=" * 60)
    print("    CITY TRANSPORT MONITOR — DAILY REPORT")
    print("=" * 60)

    for route_name, (route, trips) in routes_trips.items():
        print(f"\n--- {route_name} ---")
        print("  Segments:")
        for s in route.segments:
            print(f"    {s.name:<45} | "
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


def check_passenger_trip(city_routes, city_vehicles):
    print("\nAvailable routes:")
    route_keys = list(city_routes.keys())
    for i, key in enumerate(route_keys):
        print(f"  {i + 1}. {city_routes[key].name}")

    while True:
        try:
            route_index = int(input("Choose route number: ")) - 1
            if 0 <= route_index < len(route_keys):
                break
            print("Invalid number!")
        except ValueError:
            print("Please enter a number!")

    route_key = route_keys[route_index]
    route = city_routes[route_key]
    vehicle = city_vehicles[route_key]

    print(f"\nSegments on {route.name}:")
    for i, s in enumerate(route.segments):
        print(f"  {i + 1}. {s.name}")

    while True:
        try:
            from_index = int(input("Board at segment number: ")) - 1
            to_index = int(input("Exit at segment number: ")) - 1
            if 0 <= from_index < to_index < len(route.segments):
                break
            print("Invalid segment numbers! Make sure exit > board.")
        except ValueError:
            print("Please enter a number!")

    while True:
        try:
            departure = input("Your departure time (HH:MM): ").strip()
            departure_time = datetime.strptime(f"2024-01-01 {departure}", "%Y-%m-%d %H:%M")
            break
        except ValueError:
            print("Invalid time format! Use HH:MM")

    total_delay = timedelta()
    selected_segments = route.segments[from_index:to_index + 1]
    for segment in selected_segments:
        total_delay += vehicle.calc_delay(segment, departure_time)

    arrival_time = departure_time + total_delay

    print("\n" + "=" * 60)
    print(f"  Route:       {route.name}")
    print(f"  Vehicle:     {vehicle.get_info()}")
    print(f"  From:        {route.segments[from_index].name}")
    print(f"  To:          {route.segments[to_index].name}")
    print(f"  Departure:   {departure_time.strftime('%H:%M')}")
    print(f"  Delay:       {total_delay}")
    print(f"  Est. arrival:{arrival_time.strftime('%H:%M')}")
    print("=" * 60)


def simulate_city_day(city_routes, city_vehicles, stats):
    routes = list(city_routes.values())
    vehicles = list(city_vehicles.values())

    schedule = [
        (vehicles[0], routes[0], datetime(2024, 1, 1, 8, 0)),
        (vehicles[1], routes[1], datetime(2024, 1, 1, 8, 15)),
        (vehicles[2], routes[2], datetime(2024, 1, 1, 8, 30)),
        (vehicles[3], routes[3], datetime(2024, 1, 1, 8, 45)),
        (vehicles[0], routes[0], datetime(2024, 1, 1, 13, 0)),
        (vehicles[2], routes[2], datetime(2024, 1, 1, 13, 30)),
        (vehicles[1], routes[1], datetime(2024, 1, 1, 17, 0)),
        (vehicles[3], routes[3], datetime(2024, 1, 1, 17, 30)),
        (vehicles[0], routes[0], datetime(2024, 1, 1, 18, 0)),
    ]

    for vehicle, route, scheduled_time in schedule:
        delay = route.get_total_delay(vehicle, scheduled_time)
        actual_time = scheduled_time + delay
        stats.add_trip(Trip(vehicle, route, scheduled_time, actual_time))

def main():
    stats = Stats()
    city_routes = get_city_routes()
    city_vehicles = get_city_vehicles()
    custom_routes = list(city_routes.values())

    simulate_city_day(city_routes, city_vehicles, stats)

    print("=" * 60)
    print("      CITY TRANSPORT MONITOR — ŁÓDŹ")
    print("=" * 60)

    while True:
        print("\n1. Create custom route")
        print("2. Add trip")
        print("3. Show statistics")
        print("4. Export report to file")
        print("5. Check my trip delay")
        print("6. Exit")
        choice = input("\nChoice: ").strip()

        if choice == "1":
            route = create_route()
            custom_routes.append(route)
            print(f"\nRoute '{route.name}' created!")

        elif choice == "2":
            trip = create_trip(custom_routes)
            if trip:
                stats.add_trip(trip)
                print("Trip added!")

        elif choice == "3":
            show_statistics(stats)

        elif choice == "4":
            if not stats.trips:
                print("No trips yet!")
            else:
                filename = stats.export_report()
                print(f"Report saved to '{filename}'!")

        elif choice == "5":
            check_passenger_trip(city_routes, city_vehicles)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()