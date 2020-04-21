from typing import List, Tuple


class Route:
    def __init__(self):
        self.gps_points: List[Tuple[float, float]] = []
        self.elevations: List[Tuple[float, float, float]] = []
        self.total_distance: int = None
        self.total_duration: int = None
