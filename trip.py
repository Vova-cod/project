from datetime import datetime, timedelta

class Trip:
    def __init__(self, vehicle, route, scheduled_time: datatime, actual_time: datatime, passenger: int):
        self._vehicle = vehicle
        self._route = route
        self._scheduled_time = scheduled_time
        self._actual_time = actual_time
        self.passenger = passenger

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
    def passenger(self, value: int):
        return self._passenger

    @passenger.setter
    def passenger(self, value: int):
        self._passenger = max(0, min(value, self._vehicle.capacity))

    def get_delay(self):
        delay = self._actual_time - self._scheduled_time
        return delay if delay.total_seconds() > 0 else 0

    def get_percent(self):
        return round(self._passenger/self._vehicle.capacity * 100, 1)

    def get_info(self) -> str:
        return (f"{self._vehicle.get_info()} | "
                f"Route: {self._route.name} | "
                f"Schedule: {self._scheduled_time.strftime('%H:%M')} | "
                f"Actual time: {self._actual_time.strftime('%H:%M')} | "
                f"Delay: {self.get_delay()} | "
                f"Passengers: {self._passenger}/{self._vehicle.capacity} "
                f"({self.get_percent}%)")