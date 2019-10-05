import logging
from threading import Thread
from typing import Dict, List

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CallbackContext

from access_manager import AccessManager
from xvc.cleaning_zone import CleaningZone
from xvc.fan_level import FanLevel
from xvc.vacuum_wrapper import VacuumWrapper

# constants
SKIP_BUTTON = ['Skip']
MAIN_BUTTONS = ['Status', 'Home', 'ZoneCleaning']
FAN_BUTTONS = [value.name for value in FanLevel]

MAIN_MENU, SELECT_FAN, SELECT_ZONE = range(3)


class StatusThread(Thread):
    """
    Simple thread to get actual status from the vacuum cleaner.
    """

    def __init__(self, vacuum: VacuumWrapper) -> None:
        """
        Initializes the thread to get actual status.

        :param vacuum: Reference to vacuum cleaner.
        """
        super().__init__()
        self.daemon = True
        self.__vacuum = vacuum
        self.success = False

    def run(self) -> None:
        """
        Starts the thread.
        """
        self.success, _ = self.__vacuum.status()


class XVCBot(object):
    """
    Xiaomi Vacuum Cleaner Bot.
    """

    def __init__(self, vacuum: VacuumWrapper, zones: Dict[str, List[CleaningZone]]):
        """
        Initializes the Xiaomi Vacuum Cleaner Bot.
        This bot is used as an conversation bot with various states.

        :param vacuum: Reference to vacuum cleaner.
        :param zones: Dictionary with all cleaning zones.
        """
        self.__vacuum = vacuum
        self.__zones = zones
        self.__main_buttons = ReplyKeyboardMarkup(
            XVCBot.build_menu(MAIN_BUTTONS),
            one_time_keyboard=True)
        self.__fan_buttons = ReplyKeyboardMarkup(
            XVCBot.build_menu(FAN_BUTTONS, header_buttons=SKIP_BUTTON),
            one_time_keyboard=True)
        self.__zone_buttons = ReplyKeyboardMarkup(
            XVCBot.build_menu(sorted([zone.title() for zone in self.__zones.keys()])),
            one_time_keyboard=True)
        self.__status_thread = None

    @staticmethod
    def build_menu(buttons, columns=2, header_buttons=None, footer_buttons=None) -> List:
        """
        Creates a telegram menu with buttons.

        :param buttons: List of buttons.
        :param columns: Number of columns
        :param header_buttons: Special header buttons.
        :param footer_buttons: Special footer buttons.
        :return: List of buttons.
        """
        menu = [buttons[i:i + columns] for i in range(0, len(buttons), columns)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def __finish(self, update: Update, message: str) -> int:
        """
        Helper function to finish the conversation.

        :param update: Bot update.
        :param message: Message to send.
        :return: State for conversation end.
        """
        update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    @AccessManager()
    def start(self, update: Update, _: CallbackContext) -> int:
        """
        Starts the conversation with the main menu.

        :param update: Bot update.
        :param _: Unused parameter.
        :return: State for main menu.
        """
        logging.info('Bot command: /start')
        self.__status_thread = StatusThread(self.__vacuum)
        self.__status_thread.start()
        update.message.reply_text('Main menu', reply_markup=self.__main_buttons)
        return MAIN_MENU

    def __wait_for_status(self, update: Update) -> bool:
        """
        Waits until status thread is finish.

        :param update: Bot update.
        :return: True if connection could established.
        """
        if self.__status_thread is not None:
            if self.__status_thread.is_alive():
                update.message.reply_text('Wait for status...', reply_markup=ReplyKeyboardRemove())
                self.__status_thread.join()

        if not self.__status_thread.success:
            self.__finish(update, 'Cannot establish connection to vacuum cleaner!')
        return self.__status_thread.success

    def status(self, update: Update, _: CallbackContext) -> int:
        """
        Reads the current status of the vacuum cleaner.

        :param update: Bot update.
        :param _: Unused parameter.
        :return: State for conversation end.
        """
        if not self.__wait_for_status(update):
            return ConversationHandler.END
        logging.info('Bot command: status')
        result, state = self.__vacuum.status()
        if result:
            message = 'State: {}'.format(state)
        else:
            message = 'Error'
        return self.__finish(update, message)

    def home(self, update: Update, _: CallbackContext) -> int:
        """
        Stops cleaning and sends vacuum cleaner back to the dock.

        :param update:  Bot update.
        :param _: Unused parameter.
        :return: State for conversation end.
        """
        if not self.__wait_for_status(update):
            return ConversationHandler.END
        logging.info('Bot command: home')
        if self.__vacuum.home():
            message = 'Vacuum cleaner goes back to the dock...'
        else:
            message = 'Error'
        return self.__finish(update, message)

    def select_fan(self, update: Update, _: CallbackContext) -> int:
        """
        Creates the menu for fan speed.

        :param update: Bot update.
        :param _: Unused parameter.
        :return: State for selecting fan speed.
        """
        if not self.__wait_for_status(update):
            return ConversationHandler.END
        logging.info('Bot command: select fan')
        update.message.reply_text('Select fan speed!', reply_markup=self.__fan_buttons)
        return SELECT_FAN

    def select_zone(self, update: Update, _: CallbackContext) -> int:
        """
        Creates the menu for cleaning zones.

        :param update: Bot update.
        :param _: Unused parameter.
        :return: State for selecting cleaning zone.
        """
        logging.info('Bot command: select zone')
        level = update.message.text
        if level != SKIP_BUTTON[0]:
            self.__vacuum.set_fan_level(FanLevel[level])
        update.message.reply_text('Select zone!', reply_markup=self.__zone_buttons)
        return SELECT_ZONE

    def cleaning(self, update: Update, _: CallbackContext) -> int:
        """
        Starts cleaning.

        :param update: Bot update.
        :param _: Unused parameter.
        :return: State for conversation end.
        """
        logging.info('Bot command: cleaning')
        zone = update.message.text
        if self.__vacuum.start_zone_cleaning(self.__zones[zone.upper()]):
            message = 'Start cleaning {}...'.format(zone)
        else:
            message = 'Error'
        return self.__finish(update, message)

    def cancel(self, update: Update, _: CallbackContext) -> int:
        """
        Cancels the current conversation.

        :param update: Bot update.
        :param _: Unused parameter.
        :return: State for conversation end.
        """
        logging.info('Bot command: cancel')
        message = 'Canceled...'
        return self.__finish(update, message)
