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
            crop_area: Integer. Area available for growing crops used for food,
                in m^2.
            personnel_capacity: Integer. Maximum number of humans that can be
                supported by the facility.

        Returns:
            A new Facility instance.
        """

        self.crop_area = crop_area
        self.personnel_capacity = personnel_capacity
        self.pod_add_dict = {}
        self.in_construction = False

    def start_pod_construction(self, cur_sim_time, months_to_complete):
        """
        Schedules the completion of a new pod, adding more crop area and
        personnel capacity. Only starts construction if one is not already in
        progress.
        """
        if self.in_construction:
            # already building one
            return
        self.pod_add_dict[cur_sim_time + months_to_complete] = True
        self.in_construction = True
        return True

    def add_pod(self, cur_sim_time):
        """
        Completes the addition of a new pod, adding more crop area and
        personnel capacity.
        """
        if self.pod_add_dict.get(cur_sim_time, False):
            self.crop_area += 30000
            self.personnel_capacity += 30
            self.in_construction = False
        return True
