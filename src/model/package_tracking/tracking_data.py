from src.model.package_tracking.event import Event


class TrackingData:
    def __init__(self,
                 tracking_number,
                 status_code,
                 status_description,
                 carrier_status_code,
                 carrier_status_description,
                 ship_date,
                 estimated_delivery_date,
                 actual_delivery_date,
                 exception_description,
                 events):
        self.tracking_number = tracking_number
        self.status_code = status_code
        self.status_description = status_description
        self.carrier_status_code = carrier_status_code
        self.carrier_status_description = carrier_status_description
        self.ship_date = ship_date
        self.estimated_delivery_date = estimated_delivery_date
        self.actual_delivery_date = actual_delivery_date
        self.exception_description = exception_description
        self.events = [Event(**e) for e in events]
