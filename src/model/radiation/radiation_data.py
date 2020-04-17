import string


class RadiationData:
    def __init__(self, dose_rate):
        self.units = dose_rate["dose rate"]["units"]
        self.dose_rate = dose_rate["dose rate"]["value"]

    @property
    def radiation(self) -> string:
        return f"{self.dose_rate} {self.units}"