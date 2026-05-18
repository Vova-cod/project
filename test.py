import unittest
from datetime import datetime, timedelta
from transport import Bus, Tram
from route import Route, Segment
from trip import Trip
from statistics import Stats


class TestBus(unittest.TestCase):

    def setUp(self):
        self.segment_high_traffic = Segment("A → B", traffic_level=9,
                                            rail_condition=5, has_tram_lane=False)
        self.segment_low_traffic = Segment("A → B", traffic_level=2,
                                           rail_condition=5, has_tram_lane=False)
        self.bus = Bus("A101")

    def test_capacity(self):
        self.assertEqual(self.bus.capacity, 45)

    def test_delay_rush_hour_higher_than_daytime(self):
        rush_time = datetime(2024, 1, 1, 8, 0)
        day_time = datetime(2024, 1, 1, 13, 0)
        rush_delay = self.bus.calc_delay(self.segment_high_traffic, rush_time)
        day_delay = self.bus.calc_delay(self.segment_high_traffic, day_time)
        self.assertGreater(rush_delay, day_delay)

    def test_delay_night_lower_than_daytime(self):
        night_time = datetime(2024, 1, 1, 2, 0)
        day_time = datetime(2024, 1, 1, 13, 0)
        night_delay = self.bus.calc_delay(self.segment_high_traffic, night_time)
        day_delay = self.bus.calc_delay(self.segment_high_traffic, day_time)
        self.assertLess(night_delay, day_delay)

    def test_delay_no_traffic_is_zero(self):
        segment_no_traffic = Segment("A → B", traffic_level=1)
        day_time = datetime(2024, 1, 1, 13, 0)
        delay = self.bus.calc_delay(segment_no_traffic, day_time)
        self.assertEqual(delay, timedelta(0))

    def test_get_info_contains_number(self):
        self.assertIn("A101", self.bus.get_info())


class TestTram(unittest.TestCase):

    def setUp(self):
        self.segment_with_lane = Segment("A → B", traffic_level=8,
                                         rail_condition=4, has_tram_lane=True)
        self.segment_without_lane = Segment("A → B", traffic_level=8,
                                            rail_condition=4, has_tram_lane=False)
        self.tram = Tram("T5")

    def test_capacity(self):
        self.assertEqual(self.tram.capacity, 120)

    def test_delay_without_lane_greater_than_with_lane(self):
        day_time = datetime(2024, 1, 1, 13, 0)
        delay_with = self.tram.calc_delay(self.segment_with_lane, day_time)
        delay_without = self.tram.calc_delay(self.segment_without_lane, day_time)
        self.assertGreater(delay_without, delay_with)

    def test_delay_rush_hour_higher_than_daytime(self):
        rush_time = datetime(2024, 1, 1, 8, 0)
        day_time = datetime(2024, 1, 1, 13, 0)
        rush_delay = self.tram.calc_delay(self.segment_without_lane, rush_time)
        day_delay = self.tram.calc_delay(self.segment_without_lane, day_time)
        self.assertGreater(rush_delay, day_delay)

    def test_get_info_contains_number(self):
        self.assertIn("T5", self.tram.get_info())


class TestSegment(unittest.TestCase):

    def test_traffic_level_capped_at_10(self):
        segment = Segment("A → B", traffic_level=99)
        self.assertEqual(segment.traffic_level, 10)

    def test_traffic_level_minimum_1(self):
        segment = Segment("A → B", traffic_level=-5)
        self.assertEqual(segment.traffic_level, 1)

    def test_rail_condition_capped_at_10(self):
        segment = Segment("A → B", rail_condition=99)
        self.assertEqual(segment.rail_condition, 10)

    def test_tram_lane_default_false(self):
        segment = Segment("A → B")
        self.assertFalse(segment.has_tram_lane)

    def test_tram_lane_true(self):
        segment = Segment("A → B", has_tram_lane=True)
        self.assertTrue(segment.has_tram_lane)


class TestRoute(unittest.TestCase):

    def setUp(self):
        self.route = Route("Test Route")
        self.segment1 = Segment("A → B", traffic_level=5,
                                rail_condition=5, has_tram_lane=False)
        self.segment2 = Segment("B → C", traffic_level=5,
                                rail_condition=5, has_tram_lane=False)
        self.route.add_segment(self.segment1)
        self.route.add_segment(self.segment2)
        self.bus = Bus("A101")

    def test_segments_added(self):
        self.assertEqual(len(self.route.segments), 2)

    def test_total_delay_is_sum_of_segments(self):
        day_time = datetime(2024, 1, 1, 13, 0)
        total = self.route.get_total_delay(self.bus, day_time)
        expected = (self.bus.calc_delay(self.segment1, day_time) +
                    self.bus.calc_delay(self.segment2, day_time))
        self.assertEqual(total, expected)

    def test_empty_route_has_zero_delay(self):
        empty_route = Route("Empty")
        day_time = datetime(2024, 1, 1, 13, 0)
        self.assertEqual(empty_route.get_total_delay(self.bus, day_time), timedelta(0))


class TestTrip(unittest.TestCase):

    def setUp(self):
        self.bus = Bus("A101")
        self.route = Route("Test Route")
        self.route.add_segment(Segment("A → B", traffic_level=5,
                                       rail_condition=5, has_tram_lane=False))

    def test_delay_calculated_correctly(self):
        scheduled = datetime(2024, 1, 1, 8, 0)
        actual = datetime(2024, 1, 1, 8, 15)
        trip = Trip(self.bus, self.route, scheduled, actual)
        self.assertEqual(trip.get_delay(), timedelta(minutes=15))

    def test_early_arrival_returns_zero_delay(self):
        scheduled = datetime(2024, 1, 1, 8, 0)
        actual = datetime(2024, 1, 1, 7, 50)
        trip = Trip(self.bus, self.route, scheduled, actual)
        self.assertEqual(trip.get_delay(), timedelta(0))

    def test_passengers_within_capacity(self):
        scheduled = datetime(2024, 1, 1, 8, 0)
        actual = datetime(2024, 1, 1, 8, 10)
        trip = Trip(self.bus, self.route, scheduled, actual)
        self.assertLessEqual(trip.passengers, self.bus.capacity)
        self.assertGreaterEqual(trip.passengers, 0)

    def test_rush_hour_passengers_higher(self):
        scheduled = datetime(2024, 1, 1, 8, 0)
        actual = datetime(2024, 1, 1, 8, 10)
        trip = Trip(self.bus, self.route, scheduled, actual)
        self.assertGreaterEqual(trip.passengers, int(self.bus.capacity * 0.7))


class TestStats(unittest.TestCase):

    def setUp(self):
        self.stats = Stats()
        self.bus = Bus("A101")
        self.tram = Tram("T5")

        self.route1 = Route("Route 1")
        self.route1.add_segment(Segment("A → B", traffic_level=5,
                                        rail_condition=5, has_tram_lane=False))

        self.route2 = Route("Route 2")
        self.route2.add_segment(Segment("C → D", traffic_level=3,
                                        rail_condition=8, has_tram_lane=True))

        self.stats.add_trip(Trip(self.bus, self.route1,
                                 datetime(2024, 1, 1, 8, 0),
                                 datetime(2024, 1, 1, 8, 20)))
        self.stats.add_trip(Trip(self.tram, self.route2,
                                 datetime(2024, 1, 1, 13, 0),
                                 datetime(2024, 1, 1, 13, 10)))

    def test_average_delay(self):
        expected = (timedelta(minutes=20) + timedelta(minutes=10)) / 2
        self.assertEqual(self.stats.average_delay(), expected)

    def test_total_passengers_morning(self):
        total = self.stats.total_passengers(
            datetime(2024, 1, 1, 8, 0),
            datetime(2024, 1, 1, 10, 0)
        )
        self.assertGreater(total, 0)

    def test_total_passengers_wrong_period(self):
        total = self.stats.total_passengers(
            datetime(2024, 1, 1, 22, 0),
            datetime(2024, 1, 1, 23, 0)
        )
        self.assertEqual(total, 0)

    def test_empty_stats_average_delay(self):
        empty_stats = Stats()
        self.assertEqual(empty_stats.average_delay(), timedelta(0))

    def test_empty_stats_busiest_route(self):
        empty_stats = Stats()
        self.assertEqual(empty_stats.busiest_route(), "No data!")


if __name__ == "__main__":
    unittest.main(verbosity=2)