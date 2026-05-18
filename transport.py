from datetime import timedelta

class Transport:
    def __init__(self, number: str, capacity: int):
        self._number = number
        self._capacity = capacity

    @property
    def capacity(self):
        return self._capacity

    @property
    def number(self):
        return self._number

class Bus(Transport):
    def __init__(self, number: str, traffic_level: int = 1):
        super().__init__(number, capacity = 45)
        self.traffic_level = traffic_level

    @property
    def traffic_level(self):
        return self._traffic_level

    @traffic_level.setter
    def traffic_level(self, value: int):
        self._traffic_level = max(1, min(10, value))

    def get_info(self):
        return (f"Bus {self._number} | "
                f"Capacity: {self._capacity}")

    def calc_delay(self, segment, current_time=None):
        hour = current_time.hour if current_time else 12

        if 7 <= hour <= 9 or 17 <= hour <= 19:
            multiplier = 1.5
        elif 10 <= hour <= 16:
            multiplier = 1.0
        else:
            multiplier = 0.5
        delay_minut = int((segment.traffic_level - 1) * 2 * multiplier)
        return timedelta(minutes=delay_minut)

class Tram(Transport):
    def __init__(self, number: str, rail_condition: int = 10):
        super().__init__(number, capacity = 120)
        self.rail_condition = rail_condition

    @property
    def rail_condition(self):
        return self._rail_condition

    @rail_condition.setter
    def rail_condition(self, value: int):
        self._rail_condition = max(1, min(10, value))

    def get_info(self):
        return (f"Tram {self._number} | "
                f"Capacity: {self._capacity}")

    def calc_delay(self, segment, current_time=None):
        hour = current_time.hour if current_time else 12

        if 7 <= hour <= 9 or 17 <= hour <= 19:
            multiplier = 1.5
        elif 10 <= hour <= 16:
            multiplier = 1.0
        else:
            multiplier = 0.5

        if segment.has_tram_lane:
            delay_minut = int((10 - segment.rail_condition) * 3 * multiplier)
        else:
            delay_minut = int(((10 - segment.rail_condition) * 3 +
                                 (segment.traffic_level - 1) * 2) * multiplier)
        return timedelta(minutes=delay_minut)


vehicles = [
    Bus("А101"),
    Tram("Т5"),
    Bus("А202"),
    ]

for v in vehicles:
    print(v.get_info())