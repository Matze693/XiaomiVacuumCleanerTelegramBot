import xml.etree.ElementTree as ElementTree
from typing import Any, Type, Dict, List

from xvc_util import Point, Rectangle, Door, Room, Area


class XMLConfiguration(object):

    class TelegramBot(object):
        token = None

    class XiaomiVacuumCleanerSettings(object):
        token = None
        ip_address = None


class XMLParser(object):

    def __init__(self, path: str) -> None:
        self.__path = path
        self.__root = None
        self.reload()

    def reload(self) -> None:
        self.__root = ElementTree.parse(self.__path).getroot()

    @staticmethod
    def try_get_attribute(element: ElementTree, attribute_name: str, return_type: Any = str) -> Any:
        if attribute_name not in element.attrib:
            raise AttributeError('Attribute "{}" for element "{}" is missing!'.format(attribute_name, element.tag))
        return return_type(element.get(attribute_name))

    def parse_telegram_bot(self) -> XMLConfiguration.TelegramBot:
        result = XMLConfiguration.TelegramBot()
        result.token = self.__root.find('telegram_bot').find('token').text
        return result

    def parse_xiaomi_vacuum_cleaner_settings(self) -> XMLConfiguration.XiaomiVacuumCleanerSettings:
        result = XMLConfiguration.XiaomiVacuumCleanerSettings()
        result.token = self.__root.find('xiaomi_vacuum_cleaner').find('settings').find('token').text
        result.ip_address = self.__root.find('xiaomi_vacuum_cleaner').find('settings').find('ip_address').text
        return result

    def parse_offset(self) -> Point:
        xml_zero_point = self.__root.find('xiaomi_vacuum_cleaner').find('zone_cleaning').find('zero_point_offset')

        x = XMLParser.try_get_attribute(xml_zero_point, 'x', int)
        y = XMLParser.try_get_attribute(xml_zero_point, 'y', int)

        return Point(x, y)

    def __parse_rectangle(self, type_name: str, _type: Type[Rectangle]) -> Dict[str, Rectangle]:
        offset = self.parse_offset()

        result = dict()
        elements = self.__root.find('xiaomi_vacuum_cleaner').find('zone_cleaning').find(type_name)

        for element in elements:
            name = XMLParser.try_get_attribute(element, 'name')
            xml_bottom_left = element.find('bottom_left')
            bottom_left = Point(XMLParser.try_get_attribute(xml_bottom_left, 'x', int) + offset.x,
                                XMLParser.try_get_attribute(xml_bottom_left, 'y', int) + offset.y)
            xml_top_right = element.find('top_right')
            top_right = Point(XMLParser.try_get_attribute(xml_top_right, 'x', int) + offset.x,
                              XMLParser.try_get_attribute(xml_top_right, 'y', int) + offset.y)
            result[str(name.upper())] = _type(bottom_left, top_right, name)

        return result

    def parse_doors(self) -> Dict[str, Rectangle]:
        return self.__parse_rectangle('doors', Door)

    def parse_rooms(self) -> Dict[str, Rectangle]:
        return self.__parse_rectangle('rooms', Room)

    def parse_areas(self) -> Dict[str, Rectangle]:
        return self.__parse_rectangle('areas', Area)

    def parse_zones(self) -> Dict[str, List[Rectangle]]:
        doors = self.parse_doors()
        rooms = self.parse_rooms()
        areas = self.parse_areas()

        zones = dict()
        xml_zones = self.__root.find('xiaomi_vacuum_cleaner').find('zone_cleaning').find('zones')
        for xml_zone in xml_zones:
            name = XMLParser.try_get_attribute(xml_zone, 'name')
            elements = list()
            for element in xml_zone:
                tag = element.tag
                reference = XMLParser.try_get_attribute(element, 'name')
                if tag == 'door':
                    if reference.upper() in doors:
                        elements.append(doors[reference.upper()])
                    else:
                        raise Exception('Door "{}" does not exist!'.format(reference))
                if tag == 'room':
                    if reference.upper() in rooms:
                        elements.append(rooms[reference.upper()])
                    else:
                        raise Exception('Room "{}" does not exist!'.format(reference))
                if tag == 'area':
                    if reference.upper() in areas:
                        elements.append(areas[reference.upper()])
                    else:
                        raise Exception('Area "{}" does not exist!'.format(reference))

            zones[name.upper()] = elements

        return zones
