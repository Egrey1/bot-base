from disnake import Intents
from disnake.ext.commands import Bot
from typing import Any, Callable, Awaitable, List
import disnake

bot: Bot = ... # type: ignore
intents: Intents = ... # type: ignore
PREFIX: tuple[str] = ... # type: ignore
TOKEN: str = ... # type: ignore
VERSION: str = ... # type: ignore
test_mode: bool = ... # type: ignore

class Ask:
    @staticmethod
    def add(member_id: int, complete_handler: EventHandler | None = None, error_handler: EventHandler | None = None, checker: Callable[[disnake.Message], disnake.Embed | None] | None = None, args: list = [], kwargs: dict = {}):
        """
        Добавление поиска для пользователя

        Params:
            member_id (int): ID пользователя
            complete_handler (EventHandler | None): Обработчик успешного выбора элемента
            error_handler (EventHandler | None): Обработчик ошибки выбора элемента. Кроме сообщения передается дополнительно Embed
            checker (Callable[[disnake.Message], disnake.Embed | None] | None): Функция проверки сообщения. Если возвращает Embed, то сообщение считается ошибкой и вызывается error_handler
            args (list): Дополнительные позиционные аргументы для обработчиков
            kwargs (dict): Дополнительные именованные аргументы для обработчиков
        """

class Search:
    @staticmethod
    def add(member_id: int, title: str, items: dict[str, Any], complete_handler: EventHandler | None = None, error_handler: EventHandler | None = None, args: list = [], kwargs: dict = {}) -> disnake.Embed:
        """
        Добавление поиска для пользователя

        Params:
            member_id (int): ID пользователя
            title (str): Заголовок поиска
            items (dict[str, Any]): Словарь с элементами поиска. Ключ - название элемента, значение - экземпляр элемента
            complete_handler (EventHandler | None): Обработчик успешного выбора элемента
            error_handler (EventHandler | None): Обработчик ошибки выбора элемента. Кроме сообщения передается дополнительно Embed
            args (list): Дополнительные позиционные аргументы для обработчиков
            kwargs (dict): Дополнительные именованные аргументы для обработчиков
            
        Returns:
            disnake.Embed: Embed с элементами поиска. Его отправлять лучше сразу!
        """
        ...

class EventHandler:
    events: List[Callable[..., Any]] | None = None
    coro_events: List[Callable[..., Awaitable[Any]]] | None = None
    def __init__(self, *, event: Callable[..., Any] | None = None, coro_event: Callable[..., Awaitable[Any]] | None = None):
        """
        Создание обработчика событий

        Params:
            event (Callable[..., Any]): **Обычная функция**
            coro_event (Callable[..., Awaitable[Any]]): **Асинхронная функция**
        """
    
    def InvokeHandler(self, *args, **kwargs):
        """
        Обработка сработавшего события. В качестве аргументов принимает аргументы функций обработчиков
        """