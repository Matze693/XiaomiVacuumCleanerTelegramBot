import json
from typing import Type, Dict, List

from utility.point import Point
from utility.rectangle import Rectangle
from xvc.cleaning_zone import CleaningZone, Door, Room, Area


class Configuration(object):
    """
    Class to store configuration.
    """

    class TelegramBotSettings(object):
        """
        Class to store configuration for telegram bot.
        """
        token = None
        users = {}

    class XiaomiVacuumCleanerSettings(object):
        """
        Class to store configuration for Xiaomi Vacuum Cleaner.
        """
        simulation = None
        token = None
        ip_address = None


class ConfigurationParser(object):
    """
    Class to parse configuration.
    """

    def __init__(self, path: str) -> None:
        """
        Initialize an object of class ConfigurationParser.

        :param path: Path to configuration file.
        """
        self.__path = path
        self.__root = None
        self.reload()

    def reload(self) -> None:
        """
        Reloads the configuration file.
        """
        self.__root = json.load(open(self.__path))

    def parse_telegram_bot(self) -> Configuration.TelegramBotSettings:
        """
        Parses the telegram bot settings.

        :return: Telegram bot settings.
        """
        result = Configuration.TelegramBotSettings()
        result.token = self.__root['telegram_bot']['token']
        users = self.__root['telegram_bot']['users']
        for user in users:
            result.users[user['name']] = user['id']
        return result

    def parse_xiaomi_vacuum_cleaner_settings(self) -> Configuration.XiaomiVacuumCleanerSettings:
        """
        Parses the Xiaomi Vacuum Cleaner settings.

        :return: Xiaomi Vacuum Cleaner settings.
        """
        result = Configuration.XiaomiVacuumCleanerSettings()
        result.simulation = self.__root['xiaomi_vacuum_cleaner']['settings']['simulation']
        result.token = self.__root['xiaomi_vacuum_cleaner']['settings']['token']
        result.ip_address = self.__root['xiaomi_vacuum_cleaner']['settings']['ip_address']
        return result

    def parse_offset(self) -> Point:
        """
        Parses the x and y offset.

        :return: Offset point.
        """
        zero_point = self.__root['xiaomi_vacuum_cleaner']['zone_cleaning']['zero_point_offset']

        x = zero_point['x']
        y = zero_point['y']

        return Point(x, y)

    def __parse_cleaning_zone(self, type_name: str, _type: Type[CleaningZone]) -> Dict[str, CleaningZone]:
        """
        Parses a cleaning zone type from the configuration.

        :param type_name: Name of the cleaning zone type.
        :param _type: Cleaning zone type.
        :return: Dictionary with the cleaning zones.
        """
        offset = self.parse_offset()

        result = dict()
        elements = self.__root['xiaomi_vacuum_cleaner']['zone_cleaning'][type_name]

        for element in elements:
            name = element['name']
            config_bottom_left = element['bottom_left']
            bottom_left = Point(config_bottom_left['x'] + offset.x,
                                config_bottom_left['y'] + offset.y)
            config_top_right = element['top_right']
            top_right = Point(config_top_right['x'] + offset.x,
                              config_top_right['y'] + offset.y)
            rectangle = Rectangle(bottom_left, top_right)
            result[str(name.upper())] = _type(rectangle)

        return result

    def parse_doors(self) -> Dict[str, CleaningZone]:
        """
        Parses the doors from the configuration.

        :return: Dictionary with doors.
        """
        return self.__parse_cleaning_zone('doors', Door)

    def parse_rooms(self) -> Dict[str, CleaningZone]:
        """
        Parses the rooms from the configuration.

        :return: Dictionary with rooms.
        """
        return self.__parse_cleaning_zone('rooms', Room)

    def parse_areas(self) -> Dict[str, CleaningZone]:
        """
        Parses the areas from the configuration.

        :return: Dictionary with areas.
        """
        return self.__parse_cleaning_zone('areas', Area)

    def parse_zones(self) -> Dict[str, List[CleaningZone]]:
        """
        Parses the cleaning zones from the configuration.

        :return: Dictionary with name of zone and list of cleaning areas.
        """
        doors = self.parse_doors()
        rooms = self.parse_rooms()
        areas = self.parse_areas()

        zones = dict()
        config_zones = self.__root['xiaomi_vacuum_cleaner']['zone_cleaning']['zones']
        for config_zone in config_zones:
            name = config_zone['name']
            elements = list()

            for key in config_zone.keys():
                if key == 'doors':
                    for door in config_zone[key]:
                        reference = door['name']
                        if reference.upper() in doors:
                            elements.append(doors[reference.upper()])
                        else:
                            raise Exception('Door "{}" does not exist!'.format(reference))
                if key == 'rooms':
                    for room in config_zone[key]:
                        reference = room['name']
                        if reference.upper() in rooms:
                            elements.append(rooms[reference.upper()])
                        else:
                            raise Exception('Room "{}" does not exist!'.format(reference))
                if key == 'areas':
                    for area in config_zone[key]:
                        reference = area['name']
                        if reference.upper() in areas:
                            elements.append(areas[reference.upper()])
                        else:
                            raise Exception('Area "{}" does not exist!'.format(reference))

            zones[name.upper()] = elements

        return zones
