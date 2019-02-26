import logging

from telegram import Bot, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, Updater, CommandHandler, RegexHandler

from xml_parser import XMLParser
from xvc_helper import XVCHelper


# constants
SELECT_ZONE, _ = range(2)

# logging
logging.basicConfig(format='%(asctime)s - %(levelname)6s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class XiaomiBot(object):

    def __init__(self, xml_parser: XMLParser):
        self.__xml_parser = xml_parser
        config_xiaomi = self.__xml_parser.parse_xiaomi_vacuum_cleaner_settings()
        self.__vacuum = XVCHelper(config_xiaomi.ip_address, config_xiaomi.token)

    def start(self, bot: Bot, update: Update) -> int:
        self.__xml_parser.reload()
        zones = self.__xml_parser.parse_zones()
        buttons = [[zone.title()] for zone in zones.keys()]
        buttons = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
        update.message.reply_text('Select cleaning zone?', reply_markup=buttons)
        return SELECT_ZONE

    def select_zone(self, bot: Bot, update: Update) -> int:
        zone = update.message.text
        self.__xml_parser.reload()
        zones = self.__xml_parser.parse_zones()
        if self.__vacuum.start_zone_cleaning(zones[zone.upper()]):
            update.message.reply_text('Start cleaning {}...'.format(zone.lower()))
        else:
            update.message.reply_text('Error')
        return ConversationHandler.END

    def cancel(self, bot: Bot, update: Update) -> int:
        update.message.reply_text('Bye!', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    def error(self, bot: Bot, update: Update, message: str) -> None:
        logger.warning('Update "{}" caused error "{}"!'.format(update, message))


def main():

    # configuration
    xml_parser = XMLParser('config.xml')
    config_bot = xml_parser.parse_telegram_bot()

    xiaomi_bot = XiaomiBot(xml_parser)

    updater = Updater(token=config_bot.token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', xiaomi_bot.start)],
        states={
            SELECT_ZONE: [RegexHandler('^({})$'.format('|'.join(
                    [zone.title() for zone in xml_parser.parse_zones().keys()])), xiaomi_bot.select_zone)]
        },
        fallbacks=[CommandHandler('cancel', xiaomi_bot.cancel)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(xiaomi_bot.error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
