from enum import Enum
import logging
from typing import List, Tuple
from abc import abstractmethod, ABCMeta

from miio import Vacuum

from xvc_util import XVCListable


class XVCHelperBase(metaclass=ABCMeta):
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

    RESPONSE_SUCCEEDED = ['ok']

    @abstractmethod
    def status(self) -> Tuple[bool, str]:
        """
        Gets current status.

        :return: True on success, otherwise False.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def pause(self) -> bool:
        """
        Pause vacuum cleaner.

        :return: True on success, otherwise False.
        """
        raise NotImplementedError()

    @abstractmethod
    def home(self) -> bool:
        """
        Stops cleaning and sends vacuum cleaner back to the dock.

        :return: True on success, otherwise False.
        """
        raise NotImplementedError()

    @abstractmethod
    def start_zone_cleaning(self, zones: List[XVCListable]) -> bool:
        """
        Start the zone cleanup.

        :param zones: Different zones to clean.
        :return: True on success, otherwise False.
        """
        raise NotImplementedError()

    @abstractmethod
    def set_fan_level(self, fan_level: FanLevel) -> bool:
        """
        Sets the fan level.

        :param fan_level: New fan level.
        :return: True on success, otherwise False.
        """
        raise NotImplementedError()


class XVCHelperSimulator(XVCHelperBase):
    """
    Helper class to abstract and simplify vacuum methods.
    """

    def __init__(self, ip: str, token: str) -> None:
        """
        Initialize a object of class XVCHelper.

        :param ip: IP address of the vacuum cleaner.
        :param token: Token of the vacuum cleaner.
        """
        logging.info('Simulation: {}:{}'.format(ip, token))
        self.__ip = ip
        self.__token = token

    def status(self) -> Tuple[bool, str]:
        """
        Gets current status.

        :return: True on success, otherwise False.
        :return:
        """
        logging.info('Simulation: status()')
        return True, 'Simulation'

    def pause(self) -> bool:
        """
        Pause vacuum cleaner.

        :return: True on success, otherwise False.
        """
        logging.info('XVCHelperSimulator: pause()')
        return True

    def home(self) -> bool:
        """
        Stops cleaning and sends vacuum cleaner back to the dock.

        :return: True on success, otherwise False.
        """
        logging.info('Simulation: home()')
        return True

    def start_zone_cleaning(self, zones: List[XVCListable]) -> bool:
        """
        Start the zone cleanup.

        :param zones: Different zones to clean.
        :return: True on success, otherwise False.
        """
        logging.info('Simulation: start_zone_cleaning()')
        for zone in zones:
            logging.info('Simulation: {}'.format(zone))
        return True

    def set_fan_level(self, fan_level: XVCHelperBase.FanLevel) -> bool:
        """
        Sets the fan level.

        :param fan_level: New fan level.
        :return: True on success, otherwise False.
        """
        logging.info('Simulation: set_fan_level()')
        return True


class XVCHelper(XVCHelperBase):
    """
    Helper class to abstract and simplify vacuum methods.
    """

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
        return result == XVCHelper.RESPONSE_SUCCEEDED

    def home(self) -> bool:
        """
        Stops cleaning and sends vacuum cleaner back to the dock.

        :return: True on success, otherwise False.
        """
        result = self.__vacuum.home()
        return result == XVCHelper.RESPONSE_SUCCEEDED

    def start_zone_cleaning(self, zones: List[XVCListable]) -> bool:
        """
        Start the zone cleanup.

        :param zones: Different zones to clean.
        :return: True on success, otherwise False.
        """
        zones_list = [zone.get_list() for zone in zones]
        result = self.__vacuum.zoned_clean(zones_list)
        # self.pause()  # for debugging
        return result == XVCHelper.RESPONSE_SUCCEEDED

    def set_fan_level(self, fan_level: XVCHelperBase.FanLevel) -> bool:
        """
        Sets the fan level.

        :param fan_level: New fan level.
        :return: True on success, otherwise False.
        """
        result = self.__vacuum.set_fan_speed(fan_level.value)
        return result == XVCHelper.RESPONSE_SUCCEEDED
