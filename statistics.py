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
            route_loads[route_name].append(trip.get_load_percentage())

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

