from enum import Enum
from typing import List, Tuple

from miio import Vacuum

from xvc_util import XVCListable


class XVCHelper(object):
    """
    Helper class to abstract and simplify vacuum methods.
    """

    class FanLevel(Enum):
        """
        Enum for distinct fan levels.
        """
        Quiet = 38
        Balanced = 60
        Turbo = 75
        Max = 100
        Mob = 105

    __RESPONSE_SUCCEEDED = ['ok']

    def __init__(self, ip: str, token: str) -> None:
        """
        Initialize a object of class XVCHelper.

        :param ip: IP address of the vacuum cleaner.
        :param token: Token of the vacuum cleaner.
        """
        self.__vacuum = Vacuum(ip=ip, token=token, start_id=1)

    def status(self) -> Tuple[bool, str]:
        """
        Gets current status.

        :return: True on success, otherwise False.
        :return:
        """
        vacuum_status = self.__vacuum.status()
        return True, vacuum_status.state

    def pause(self) -> bool:
        """
        Pause vacuum cleaner.

        :return: True on success, otherwise False.
        """
        result = self.__vacuum.pause()
        return result == XVCHelper.__RESPONSE_SUCCEEDED

    def start_zone_cleaning(self, zones: List[XVCListable]) -> bool:
        """
        Start the zone cleanup.

        :param zones: Different zones to clean.
        :return: True on success, otherwise False.
        """
        zones_list = [zone.get_list() for zone in zones]
        result = self.__vacuum.zoned_clean(zones_list)
        # self.pause()  # for debugging
        return result == XVCHelper.__RESPONSE_SUCCEEDED

    def set_fan_level(self, fan_level: FanLevel) -> bool:
        """
        Sets the fan level.

        :param fan_level: New fan level.
        :return: True on success, otherwise False.
        """
        result = self.__vacuum.set_fan_speed(fan_level.value)
        return result == XVCHelper.__RESPONSE_SUCCEEDED
