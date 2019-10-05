from typing import List, Tuple

from miio import Vacuum, DeviceException

from xvc.cleaning_zone import CleaningZone
from xvc.fan_level import FanLevel


class VacuumWrapper(object):
    """
    Wrapper class to abstract and simplify vacuum methods.
    """

    RESPONSE_SUCCEEDED = ['ok']

    def __init__(self, vacuum: Vacuum):
        """
        Initialize a object of class VacuumWrapper.

        :param vacuum: Vacuum reference.
        """
        self.__vacuum = vacuum

        # check connection
        for _ in range(3):
            try:
                self.__vacuum.do_discover()
                break
            except DeviceException:
                continue
        else:
            raise ConnectionError('Cannot establish connection to Vacuum Cleaner at {}'.format(self.__vacuum.ip))

    def status(self) -> Tuple[bool, str]:
        """
        Gets current status.

        :return: True on success, otherwise false.
        :return: Vacuum status.
        """
        vacuum_status = None
        try:
            vacuum_status = self.__vacuum.status().state
            result = True
        except DeviceException:
            result = False
        return result, vacuum_status

    def pause(self) -> bool:
        """
        Pause vacuum cleaner.

        :return: True on success, otherwise False.
        """
        result = self.__vacuum.pause()
        return result == VacuumWrapper.RESPONSE_SUCCEEDED

    def home(self) -> bool:
        """
        Stops cleaning and sends vacuum cleaner back to the dock.

        :return: True on success, otherwise False.
        """
        result = self.__vacuum.home()
        return result == VacuumWrapper.RESPONSE_SUCCEEDED

    def start_zone_cleaning(self, zones: List[CleaningZone]) -> bool:
        """
        Start the zone cleanup.

        :param zones: Different zones to clean.
        :return: True on success, otherwise False.
        """
        self.pause()
        zones_list = [zone.get_list() for zone in zones]
        result = self.__vacuum.zoned_clean(zones_list)
        return result == VacuumWrapper.RESPONSE_SUCCEEDED

    def set_fan_level(self, fan_level: FanLevel) -> bool:
        """
        Sets the fan level.

        :param fan_level: New fan level.
        :return: True on success, otherwise False.
        """
        result = self.__vacuum.set_fan_speed(fan_level.value)
        return result == VacuumWrapper.RESPONSE_SUCCEEDED
