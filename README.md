# XiaomiVacuumCleanerTelegramBot
A useful telegram bot to control Xiaomi Vacuum Cleaner V2.

## Motivation
The Xiaomi Vacuum Cleaner V2 has the new cleaning zone feature. This is awesome and very helpful!
But unfortunately each time the cleaning zone must be reconfigured for certain rooms.
That is time-consuming and annoying.
It would be nice if I could just tell Roborock, "Clean the living room.".

## Installation
1. Install the python package [python-miio](https://github.com/rytilahti/python-miio)
2. Get your token from the Roborock (see [python-miio.readthedocs.io](https://python-miio.readthedocs.io/en/latest/discovery.html))
3. Create a telegram bot with [BotFather](https://telegram.me/botfather).
4. Clone or download the XiaomiVacuumCleanerTelegramBot.
5. Make a copy of the file `example_config.xml` -> `config.xml`.
6. Insert the Roborock and Telegram Bot token into `config.xml`.
7. Insert the Roborock IP address into `config.xml`
8. Insert your cleaning zones (doors, rooms, areas) in the `config.xml`.
9. Start the telegram bot with `main.py`.

## Usage
1. Start your Telegram Bot with `/start`.
2. Follow the menu.
3. Enjoy :smile:

## Need help or further ideas
Feel free to add an issue or an pull request.
