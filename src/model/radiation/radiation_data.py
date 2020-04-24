import string


UNITS = {
    "uSv/hr": 3600,
    "uSv/m": 60,
    "uSv/s": 1
}


class RadiationData:
    def __init__(self, dose_rate):
        unit = dose_rate["dose rate"]["units"]
        if unit not in UNITS:
            raise ValueError(f"Received unexpected radiation unit: {unit}")
        self.dose_rate = dose_rate["dose rate"]["value"] / UNITS[unit]
        self.unit = "uSv/s"

    @property
    def radiation(self) -> string:
        return f"{self.dose_rate} {self.unit}"
