from datetime import timedelta

class Segment:
    def __init__(self, name: str, traffic_level: int = 1, rail_condition: int = 10, has_tram_lane: bool = False):
        self._name = name
        self.traffic_level = traffic_level
        self.rail_condition = rail_condition
        self.has_tram_lane = has_tram_lane

    @property
    def name(self):
        return self._name

    @property
    def traffic_level(self):
        return self._traffic_level

    @traffic_level.setter
    def traffic_level(self, value: int):
        self._traffic_level = max(1, min(value, 10))

    @property
    def rail_condition(self):
        return self._rail_condition

    @rail_condition.setter
    def rail_condition(self, value: int):
        self._rail_condition = max(1, min(value, 10))

    def get_info(self):
        return (f"Segment: {self._name} |"
                f" Traffic Level: {self.traffic_level}/10 |"
                f" Rail Condition: {self.rail_condition}/10 |"
                f" Tram Lane: {"yes" if self.has_tram_lane else "no"}")


class Route:
    def __init__(self, name: str):
        self._name = name
        self._segments = []

    @property
    def name(self):
        return self._name

    @property
    def segments(self):
        return self._segments

    def add_segment(self, segment: Segment):
        return self._segments.append(segment)

    def get_total_delay(self, vehicle, current_time=None):
        total_delay = timedelta()
        for segment in self._segments:
            total_delay += vehicle.calc_delay(segment, current_time)
        return total_delay

    def get_info(self):
        return (f"Route: {self._name} |"
                f"Segments: len({self.segments})")