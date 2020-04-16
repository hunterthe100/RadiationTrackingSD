class Part:
    def __init__(self,
                 part_id: str,
                 part_name: str,
                 package_id: str,
                 part_radiation: str):
        self.part_id: str = part_id
        self.part_name: str = part_name
        self.package_id: str = package_id
        self.part_radiation: str = part_radiation
