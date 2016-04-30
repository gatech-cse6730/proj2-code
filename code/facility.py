class Facility(object):
    """
    The Facility class is used for modeling the "facilities"
    occupied by a given population. The facilities entail
    living quarters, area for growing crops, power generation
    machinery, and more.

    """

    def __init__(self, crop_area, personnel_capacity):
        """
        Creates a new Facility.

        Args:
            crop_area: Integer. Area available for growing crops used
                       for food, in m^2.
            personnel_capacity: Integer. Maximum number of humans that
                                can be supported by the facility.

        Returns:
            A new Facility instance.

        """

        self.crop_area = crop_area
        self.personnel_capacity = personnel_capacity