from src.dao.data_access_object_package_tracking import DataAccessObjectPackageTracking
from src.model.package_tracking.event import Event
from src.model.package_tracking.tracking_data import TrackingData

package_tracking_dao = DataAccessObjectPackageTracking()

carrier_code = "fedex"
tracking_number = "120667023892"
tracking_data: TrackingData = package_tracking_dao.get_tracking_data(carrier_code, tracking_number)
