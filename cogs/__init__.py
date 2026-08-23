import logging
import dependencies as deps
from os import listdir

for foldername in listdir('./cogs'):
    if not foldername.startswith('__'):
        try:
            deps.bot.load_extension(f'cogs.{foldername}')
            logging.info(f'Загружено расширение {foldername}')
        except Exception as e:
            logging.error(f'При загрузке расширения {foldername} произошла ошибка: {e}')