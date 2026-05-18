from datetime import datetime, timedelta
import random

class Trip:
    def __init__(self, vehicle, route, scheduled_time: datetime, actual_time: datetime):
        self._vehicle = vehicle
        self._route = route
        self._scheduled_time = scheduled_time
        self._actual_time = actual_time
        self._passengers = self._generate_passengers()

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def route(self):
        return self._route

    @property
    def scheduled_time(self):
        return self._scheduled_time

    @property
    def actual_time(self):
        return self._actual_time

    @property
    def passengers(self):
        return self._passengers

    def _generate_passengers(self) -> int:
        hour = self._actual_time.hour
        capacity = self._vehicle.capacity

        if 7 <= hour <= 9 or 17 <= hour <= 19:
            return random.randint(int(capacity * 0.7), capacity)
        elif 10 <= hour <= 16:
            return random.randint(int(capacity * 0.3), int(capacity * 0.6))
        else:
            return random.randint(0, int(capacity * 0.3))

    def get_delay(self):
        delay = self._actual_time - self._scheduled_time
        return delay if delay.total_seconds() > 0 else timedelta(0)

    def get_percent(self):
        return round(self._passengers/self._vehicle.capacity * 100, 1)

    def get_info(self):
        segments_info = ", ".join(
            f"{s.name} (tram lane: {'yes' if s.has_tram_lane else 'no'})"
            for s in self._route.segments
        )
        return (f"{self._vehicle.get_info()} | "
                f"Route: {self._route.name} | "
                f"Segments: {segments_info} | "
                f"Schedule: {self._scheduled_time.strftime('%H:%M')} | "
                f"Actual time: {self._actual_time.strftime('%H:%M')} | "
                f"Delay: {self.get_delay()} | "
                f"Passengers: {self.get_percent()}%")