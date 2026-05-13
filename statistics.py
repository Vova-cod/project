from datetime import datetime, timedelta

class Stats:
    def __init__(self):
        self._trips = []

    @property
    def trips(self):
        return self._trips

    def add_trip(self, trip):
        self._trips.append(trip)

    def average_delay(self):
        if not self._trips:
            return timedelta(0)

        total = timedelta(0)
        for trip in self._trips:
            total += trip.get_delay()

        return total / len(self._trips)

    def total_passengers(self, start_time: datetime, end_time: datetime):
        total = 0
        for trip in self._trips:
            if start_time <= trip.actual_time <= end_time:
                total += trip.passengers
        return total

    def busiest_route(self):
        if not self._trips:
            return "No data!"

        route_loads = {}
        for trip in self._trips:
            route_name = trip.route.name
            if route_name not in route_loads:
                route_loads[route_name] = []
            route_loads[route_name].append(trip.get_percent())

        average_loads = {}
        for route_name, loads in route_loads.items():
            average_loads[route_name] = sum(loads) / len(loads)

        return max(average_loads, key=average_loads.get)

    def get_report(self, start_time: datetime, end_time: datetime):
        return (f"Period: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} |"
                f"Routs: {len(self._trips)} | "
                f"Average delay: {self.average_delay()} | "
                f"Passengers: {self.total_passengers(start_time, end_time)} | "
                f"Busiest route: {self.busiest_route()}")

    def export_report(self):
        now = datetime.now()
        filename = f"report_{now.strftime('%Y-%m-%d_%H-%M')}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("    CITY TRANSPORT MONITOR — DAILY REPORT\n")
            f.write(f"    Generated: {now.strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 60 + "\n")

            routes_trips = {}
            for trip in self._trips:
                route_name = trip.route.name
                if route_name not in routes_trips:
                    routes_trips[route_name] = (trip.route, [])
                routes_trips[route_name][1].append(trip)

            for route_name, (route, trips) in routes_trips.items():
                f.write(f"\n--- {route_name} ---\n")

                f.write("  Segments:\n")
                for s in route.segments:
                    f.write(f"    {s.name:<40} | "
                            f"Traffic: {s.traffic_level}/10 | "
                            f"Rail: {s.rail_condition}/10 | "
                            f"Tram lane: {'yes' if s.has_tram_lane else 'no'}\n")

                f.write("  Trips:\n")
                for trip in trips:
                    f.write(f"    {trip.vehicle.get_info()} | "
                            f"Schedule: {trip.scheduled_time.strftime('%H:%M')} | "
                            f"Actual: {trip.actual_time.strftime('%H:%M')} | "
                            f"Delay: {trip.get_delay()} | "
                            f"Passengers: {trip.get_percent()}%\n")

            f.write("\n" + "=" * 60 + "\n")
            f.write("  STATISTICS:\n")
            f.write(f"  Total trips:        {len(self._trips)}\n")
            f.write(f"  Average delay:      {self.average_delay()}\n")
            f.write(f"  Busiest route:      {self.busiest_route()}\n")

        return filename

