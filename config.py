import dependencies as deps
import disnake as ds
import disnake.user as ds_user
from disnake.ext.commands import Bot
from dotenv import load_dotenv
from os import getenv
import sqlite3 as sql
import logging

def first_config():
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    deps.PREFIX = ('!', '! ')
    deps.bot = Bot(
        command_prefix=deps.PREFIX, 
        intents=ds.Intents.all(), 
        sync_commands=True, 
        allowed_mentions=ds.AllowedMentions.none(),
        help_command=None,
        strip_after_prefix=True
    )
    import classes as cls
    
    deps.TOKEN = getenv('TOKEN')
    deps.test_mode = bool(getenv('test_mode'))
    deps.VERSION = '0.0 Тесты'
    
    deps.EventHandler = cls.EventHandler
    deps.Search = cls.Search
    

async def second_config():
    import cogs as _
    logging.info(f'Бот успешно запущен как {deps.bot.user}')
    logging.info(f'Количество загруженных когов/расширений: {len(deps.bot.cogs)}')
    logging.info(f'Количество доступных команд: {len(deps.bot.all_commands)}')
    logging.info(f'Список всех команд: ' + ', '.join(deps.bot.all_commands.keys()))
    logging.info(f'Версия бота: {deps.VERSION}')
