from typing import List

from src.model.part import Part


class Package:
    def __init__(self):
        self.package_id: str = None
        self.carrier_code: str = None
        self.tracking_number: str = None
        self.package_radiation: str = None
        self.delivered = None
        self.parts: List[Part] = []
