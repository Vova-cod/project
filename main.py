from datetime import datetime
from transport import Bus, Tram
from route import Route, Segment
from trip import Trip
from statistics import Stats


def create_route():
    name = input("Route name: ")
    route = Route(name)

    while True:
        print("\n  1. Add segment")
        print("  2. Finish route")
        choice = input("Choice: ")

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
            segment = Segment(seg_name, traffic_level=traffic,
                              rail_condition=rail, has_tram_lane=tram_lane)
            route.add_segment(segment)
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

    if transport_type == "bus":
        vehicle = Bus(number)
    else:
        vehicle = Tram(number)

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


def main():
    stats = Stats()
    routes = []

    print("=" * 60)
    print("      CITY TRANSPORT MONITOR")
    print("=" * 60)

    while True:
        print("\n1. Create route")
        print("2. Add trip")
        print("3. Show statistics")
        print("4. Export report to file")
        print("5. Exit")
        choice = input("\nChoice: ").strip()

        if choice == "1":
            route = create_route()
            routes.append(route)
            print(f"\nRoute '{route.name}' created!")

        elif choice == "2":
            trip = create_trip(routes)
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
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()