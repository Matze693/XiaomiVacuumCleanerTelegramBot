import logging
from typing import List
from unittest.mock import Mock

from xvc.vacuum_wrapper import VacuumWrapper


class VacuumMock(Mock):
    """
    Mock class to simulate vacuum driver.
    """

    def __log(self, message: str) -> None:
        logging.debug('{}: {}'.format(self.__class__.__name__, message))

    def home(self) -> str:
        return VacuumWrapper.RESPONSE_SUCCEEDED

    def zoned_clean(self, zones: List[List[int]]) -> str:
        self.__log('zone cleaning: {}'.format(zones))
        return VacuumWrapper.RESPONSE_SUCCEEDED
