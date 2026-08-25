from typing import Any, Callable, Awaitable, List
from disnake import Embed, Colour, Message
from disnake.ext.commands import Context
import dependencies as deps
import logging
import asyncio
import disnake
from disnake.ext import commands
# Тут с импортами я переборщил чутка, в смысле где-то они абсолютные, где-то релативные

# Создаем новый класс с двумя полями: events, coro_events
# Это основа для Собыйтино-Управляемого Программирования (СУП)
class EventHandler:
    events: List[Callable[..., Any]] | None = None
    coro_events: List[Callable[..., Awaitable[Any]]] | None = None

    # В конструкторе мы этим двум полям задаем значения, чтобы потом их использовать в обработчике событий
    def __init__(self, event = None, coro_event = None):
        self.events = [event] if not isinstance(event, list) and event is not None else event if event else None
        self.coro_events = [coro_event] if not isinstance(coro_event, list) and coro_event is not None else coro_event if coro_event else None
    
    # запускаем все функции
    async def invokeHandler(self, *args, **kwargs):
        if self.events:
            for event in self.events:
                event(*args, **kwargs)
        if self.coro_events:
            for coro_event in self.coro_events:
                await coro_event(*args, **kwargs)
    
    # Добавляем новое обычное событие
    def add_event(self, event):
        if not self.events:
            self.events = [event]
        else:
            self.events.append(event)

    # Добавляем новое событие с корутиной
    def add_coro_event(self, event):
        if not self.coro_events:
            self.coro_events = [event]
        else:
            self.coro_events.append(event)
    
    # Классовый метод, чтобы возвращался всегда EventHandler
    @classmethod
    def copy(cls, event: 'EventHandler | None'):
        if event:
            return cls(event.events, event.coro_events)
        else:
            return cls(None, None)

# Статический класс для события спрашивания. Когда бот задает вопрос и ему нужно получить текстовый ответ
class Ask(commands.Cog):
    members: dict[int, tuple[EventHandler, EventHandler, Callable[[disnake.Message], Awaitable[disnake.Embed | None]] | None, list, dict, bool]] = {}
    # Список со всеми пользователями для их обработки. Да, такое решение нагружает систему, но это компенсируется очисткой пользователя, если он не отвечает уже как 5 минут
    
    # Добавить нового пользователя в базу 
    @staticmethod
    def add(member_id: int, complete_handler: EventHandler | None = None, error_handler: EventHandler | None = None, checker: Callable[[disnake.Message], Awaitable[disnake.Embed | None]] | None = None, *, args: list = [], kwargs: dict = {}, bounce: bool = False):
        # Делаем EventHandler и привязываем его к пользователю
        complete_handler = EventHandler.copy(complete_handler)
        error_handler = EventHandler.copy(error_handler)
        Ask.members[member_id] = (complete_handler, error_handler, checker, args, kwargs, bounce)
        # Если пользователь не отвечает уже как 5 минут, то его запись удаляется
        asyncio.create_task(Ask.__cancel(member_id))
    
    @staticmethod
    async def __cancel(member_id: int):
        await asyncio.sleep(5 * 60)
        if member_id in Ask.members:
            del Ask.members[member_id]
            # Запись удаляется "втихую"
    
    @commands.Cog.listener('on_message')
    async def on_message_handler(self, message: Message):
        try:
            if message.author.id not in Ask.members:
                return
            
            # Собираем все переменные для пользователя
            complete_handler, error_handler, checker, args, kwargs, bounce = Ask.members.pop(message.author.id)
            if not bounce:
                # bounce нужен, потому что в обработчик сообщений может попасться команда, которая и спровоцировала бота привязать его к событиям Ask
                Ask.members[message.author.id] = (complete_handler, error_handler, checker, args, kwargs, True)
                return
            
            checker_result = (await checker(message)) if checker else None
            
            if isinstance(checker_result, Embed):
                # Если проверка сообщения не прошла, то вызывается ошибка
                await error_handler.invokeHandler(message, checker_result, *args, **kwargs)
                return
            
            # Если все хорошо, то выполняется остальная часть бота
            await complete_handler.invokeHandler(message, *args, **kwargs)
        except Exception as e:
            await error_handler.invokeHandler(message, Embed(
                title='Неизвестная ошибка',
                description='Проверьте доступность прав бота',
                colour=Colour.red()
            ), *args, **kwargs)
            logging.error(e)
            
# еще один статический класс. Он наследуется от Ask
class Search(Ask): 
    # Мы делаем свой успешный обработчик, чтобы передать выбранный предмет в пользовательскую функцию
    @staticmethod
    async def __search_complete_handler(message: disnake.Message, items: dict[str, Any], complete_handler: EventHandler, _, *args: list, **kwargs: dict):
        item = list(items.keys())[int(message.content) - 1]
        await complete_handler.invokeHandler(message, item, *args, **kwargs)
    
    # Здесь такая же логика
    @staticmethod
    async def __search_cancel_handler(message: disnake.Message, embed: Embed, _, __, error_handler: EventHandler, *args, **kwargs):
        await error_handler.invokeHandler(message, embed, *args, **kwargs)
    
    @staticmethod
    def add(member_id: int, title: str, items: dict[str, Any], complete_handler: EventHandler | None = None, error_handler: EventHandler | None = None, *, args: list = [], kwargs: dict = {}):
        if len(items) == 0:
            raise ValueError('В Search.add() был передан пустой словарь')
            
        search_complete_handler = EventHandler(coro_event=Search.__search_complete_handler)
        search_cancel_handler = EventHandler(coro_event=Search.__search_cancel_handler)
        
        # Создаем свою проверку. Делаем ответ только для чисел в нужном диапозоне 
        async def checker(message: disnake.Message):
            num = 0
            try:
                num = int(message.content)
            except ValueError:
                return Embed(
                    title='Ошибка',
                    description='Вы должны ввести число',
                    colour=Colour.red()
                )
            if num < 1 or num > len(items):
                return Embed(
                    title='Ошибка',
                    description=f'Вы должны ввести число от 1 до {len(items)}',
                    colour=Colour.red()
                )
                
        # Вот так страшно это все передаем
        Ask.add(member_id, search_complete_handler, search_cancel_handler, checker, args=([items, complete_handler, error_handler] + args), kwargs=kwargs)
        
        # И строим эмбеды
        embeds = []
        embeds.append(Embed(
            title=title,
            description='\n'.join([f'**{i + 1}.** {item}' for i, item in enumerate(items.keys())])
        ))
        for i in range(1, (len(items) // 50) + 1):
            embeds.append(Embed(
                description='\n'.join([f'**{j + 1}.** {item}' for j, item in enumerate(items.keys())])
            ))
            
        # Напоминаю, боту лучше отправлять по пять таких
        return embeds


deps.bot.add_cog(Ask())