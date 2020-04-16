
class Event:
    def __init__(self,
                 occurred_at,
                 carrier_occurred_at,
                 description,
                 city_locality,
                 state_province,
                 postal_code,
                 country_code,
                 company_name,
                 signer,
                 event_code,
                 latitude,
                 longitude):
        self.occurred_at = occurred_at
        self.carrier_occurred_at = carrier_occurred_at
        self.description = description
        self.city_locality = city_locality
        self.state_province = state_province
        self.postal_code = postal_code
        self.country_code = country_code
        self.company_name = company_name
        self.signer = signer
        self.event_code = event_code
        self.latitude = latitude
        self.longitude = longitude
