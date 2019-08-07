import logging

from telegram.ext import ConversationHandler, Updater, CommandHandler, RegexHandler

from access_manager import AccessManager
from json_parser import ConfigurationParser
from xvc_bot import XVCBot, MAIN_MENU, SELECT_FAN, SELECT_ZONE, FAN_BUTTONS, SKIP_BUTTON
from xvc_helper import XVCHelper, XVCHelperSimulator

# constants
LOG_FILE = 'bot.log'
LOG_DISABLE = 100

# logging
logging.getLogger('telegram').setLevel(LOG_DISABLE)

console_logging = logging.StreamHandler()
console_logging.setLevel(logging.ERROR)

file_logging = logging.FileHandler(LOG_FILE)
file_logging.setLevel(logging.NOTSET)

logging.basicConfig(level=logging.NOTSET,
                    handlers=[console_logging, file_logging],
                    format='%(asctime)23s - %(levelname)8s - %(name)25s - %(funcName)25s - %(message)s'
                    )


# main program
def main():
    # configuration
    parser = ConfigurationParser('config.json')
    config_bot = parser.parse_telegram_bot()

    AccessManager.add_users(config_bot.users.values())

    config_xiaomi = parser.parse_xiaomi_vacuum_cleaner_settings()

    vacuum = None
    try:
        if config_xiaomi.simulation:
            vacuum = XVCHelperSimulator(config_xiaomi.ip_address, config_xiaomi.token)
        else:
            vacuum = XVCHelper(config_xiaomi.ip_address, config_xiaomi.token)
    except ConnectionError as ex:
        logging.fatal(str(ex))
        exit()

    zones = parser.parse_zones()

    xvc_bot = XVCBot(vacuum, zones)

    updater = Updater(token=config_bot.token)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', xvc_bot.start)],
        states={
            MAIN_MENU: [RegexHandler('^({})$'.format('Status'),
                                     xvc_bot.status),
                        RegexHandler('^({})$'.format('Home'),
                                     xvc_bot.home),
                        RegexHandler('^({})$'.format('ZoneCleaning'),
                                     xvc_bot.select_fan)],
            SELECT_FAN: [RegexHandler('^({})$'.format('|'.join(FAN_BUTTONS + SKIP_BUTTON)),
                                      xvc_bot.select_zone)],
            SELECT_ZONE: [RegexHandler('^({})$'.format('|'.join([zone.title() for zone in zones.keys()])),
                                       xvc_bot.cleaning)]
        },
        fallbacks=[CommandHandler('cancel', xvc_bot.cancel)]
    )

    dispatcher.add_handler(conversation_handler)

    logging.info('start bot')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.info('start program')
    main()
