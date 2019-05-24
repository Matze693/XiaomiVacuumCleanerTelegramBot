import logging
from typing import List, Dict, Callable

from telegram import Update


class AccessManager(object):
    __valid_users = []

    @classmethod
    def add_users(cls, users: List) -> None:
        """
        Adds new users to the list with valid users.

        :param users: List with user ids.
        """
        cls.__valid_users.extend(users)

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: List, **kwargs: Dict):
            update = None
            for arg in (args + tuple(kwargs.values())):
                if isinstance(arg, Update):
                    update = arg
                    break
            if update is None:
                logging.critical('No argument has type "Update"!')
            else:
                user_id = update.effective_user.id
                if user_id not in self.__valid_users:
                    logging.warning('AccessManager: Access denied for {}'.format(user_id))
                    update.message.reply_text('Access denied for you ({})!'.format(user_id))
                    return
                else:
                    return func(*args, **kwargs)

        return wrapper
