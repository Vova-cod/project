from transport import Bus, Tram
from route import Route, Segment


def get_city_routes():

    tram_6 = Route("Tram Line 6 (Pl. Niepodległości → Retkinia)")
    tram_6.add_segment(Segment("Pl. Niepodległości → Pl. Wolności",
                                traffic_level=7, rail_condition=6, has_tram_lane=True))
    tram_6.add_segment(Segment("Pl. Wolności → Piotrkowska-Centrum",
                                traffic_level=8, rail_condition=5, has_tram_lane=False))
    tram_6.add_segment(Segment("Piotrkowska-Centrum → Pl. Reymonta",
                                traffic_level=6, rail_condition=7, has_tram_lane=True))
    tram_6.add_segment(Segment("Pl. Reymonta → Dw. Łódź Kaliska",
                                traffic_level=5, rail_condition=8, has_tram_lane=True))
    tram_6.add_segment(Segment("Dw. Łódź Kaliska → Retkinia",
                                traffic_level=3, rail_condition=9, has_tram_lane=True))

    tram_12 = Route("Tram Line 12 (Retkinia → Pabianicka)")
    tram_12.add_segment(Segment("Retkinia → Dw. Łódź Kaliska",
                                 traffic_level=3, rail_condition=8, has_tram_lane=True))
    tram_12.add_segment(Segment("Dw. Łódź Kaliska → Pl. Reymonta",
                                 traffic_level=5, rail_condition=6, has_tram_lane=True))
    tram_12.add_segment(Segment("Pl. Reymonta → Piotrkowska-Centrum",
                                 traffic_level=8, rail_condition=4, has_tram_lane=False))
    tram_12.add_segment(Segment("Piotrkowska-Centrum → Rondo Solidarności",
                                 traffic_level=7, rail_condition=5, has_tram_lane=False))
    tram_12.add_segment(Segment("Rondo Solidarności → Pabianicka",
                                 traffic_level=4, rail_condition=7, has_tram_lane=True))

    bus_55 = Route("Bus Line 55 (Dw. Łódź Fabryczna → Łagiewniki)")
    bus_55.add_segment(Segment("Dw. Łódź Fabryczna → Kilińskiego",
                                traffic_level=8, rail_condition=5, has_tram_lane=False))
    bus_55.add_segment(Segment("Kilińskiego → Pl. Wolności",
                                traffic_level=7, rail_condition=5, has_tram_lane=False))
    bus_55.add_segment(Segment("Pl. Wolności → Zgierska",
                                traffic_level=6, rail_condition=6, has_tram_lane=False))
    bus_55.add_segment(Segment("Zgierska → Dw. Łódź Radogoszcz",
                                traffic_level=4, rail_condition=7, has_tram_lane=False))
    bus_55.add_segment(Segment("Dw. Łódź Radogoszcz → Łagiewniki",
                                traffic_level=2, rail_condition=8, has_tram_lane=False))

    # --- BUS LINE 51A (Dw. Łódź Fabryczna → Chojny) ---
    bus_51a = Route("Bus Line 51A (Dw. Łódź Fabryczna → Chojny)")
    bus_51a.add_segment(Segment("Dw. Łódź Fabryczna → Piotrkowska-Centrum",
                                 traffic_level=9, rail_condition=5, has_tram_lane=False))
    bus_51a.add_segment(Segment("Piotrkowska-Centrum → Rondo Solidarności",
                                 traffic_level=8, rail_condition=5, has_tram_lane=False))
    bus_51a.add_segment(Segment("Rondo Solidarności → Rzgowska",
                                 traffic_level=6, rail_condition=6, has_tram_lane=False))
    bus_51a.add_segment(Segment("Rzgowska → Dw. Łódź Chojny",
                                 traffic_level=4, rail_condition=7, has_tram_lane=False))

    return {
        "tram_6": tram_6,
        "tram_12": tram_12,
        "bus_55": bus_55,
        "bus_51a": bus_51a
    }


def get_city_vehicles():
    return {
        "tram_6": Tram("T6"),
        "tram_12": Tram("T12"),
        "bus_55": Bus("B55"),
        "bus_51a": Bus("B51A")
    }