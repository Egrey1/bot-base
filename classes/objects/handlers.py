from typing import Any, Callable, Awaitable, List

from ..library import Embed, Colour, Context, Message, deps, logging, asyncio
import disnake
from disnake.ext import commands

class EventHandler:
    events: List[Callable[..., Any]] | None = None
    coro_events: List[Callable[..., Awaitable[Any]]] | None = None

    def __init__(self, event = None, coro_event = None):
        self.events = [event] if not isinstance(event, list) and event is not None else event if event else None
        self.coro_events = [coro_event] if not isinstance(coro_event, list) and coro_event is not None else coro_event if coro_event else None

    async def invokeHandler(self, *args, **kwargs):
        if self.events:
            for event in self.events:
                event(*args, **kwargs)
        if self.coro_events:
            for coro_event in self.coro_events:
                await coro_event(*args, **kwargs)
    
    def add_event(self, event):
        if not self.events:
            self.events = [event]
        else:
            self.events.append(event)

    def add_coro_event(self, event):
        if not self.coro_events:
            self.coro_events = [event]
        else:
            self.coro_events.append(event)
    
    @classmethod
    def copy(cls, event: 'EventHandler | None'):
        if event:
            return cls(event.events, event.coro_events)
        else:
            return cls(None, None)

class Ask(commands.Cog):
    members: dict[int, tuple[EventHandler, EventHandler, Callable[[disnake.Message], disnake.Embed | None] | None, list, dict, bool]] = {}
    
    @staticmethod
    def add(member_id: int, complete_handler: EventHandler | None = None, error_handler: EventHandler | None = None, checker: Callable[[disnake.Message], disnake.Embed | None] | None = None, args: list = [], kwargs: dict = {}, bounce: bool = False):
        complete_handler = EventHandler.copy(complete_handler)
        error_handler = EventHandler.copy(error_handler)
        Ask.members[member_id] = (complete_handler, error_handler, checker, args, kwargs, bounce)
        asyncio.create_task(Ask.__cancel(member_id))
    
    @staticmethod
    async def __cancel(member_id: int):
        await asyncio.sleep(5 * 60)
        if member_id in Ask.members:
            del Ask.members[member_id]
    
    @commands.Cog.listener('on_message')
    async def on_message_handler(self, message: Message):
        try:
            if message.author.id not in Ask.members:
                return
            
            complete_handler, error_handler, checker, args, kwargs, bounce = Ask.members.pop(message.author.id)
            if not bounce:
                Ask.members[message.author.id] = (complete_handler, error_handler, checker, args, kwargs, True)
                return
            
            checker_result = checker(message) if checker else None
            
            if isinstance(checker_result, Embed):
                await error_handler.invokeHandler(message, checker_result, *args, **kwargs)
                return
            
            await complete_handler.invokeHandler(message, *args, **kwargs)
        except Exception as e:
            await error_handler.invokeHandler(message, Embed(
                title='Неизвестная ошибка',
                description='Проверьте доступность прав бота',
                colour=Colour.red()
            ), *args, **kwargs)
            logging.error(e)
            

class Search(Ask): 
    @staticmethod
    async def __search_complete_handler(message: disnake.Message, items: dict[str, Any], complete_handler: EventHandler, *args: list, **kwargs: dict):
        item = list(items.keys())[int(message.content) - 1]
        await complete_handler.invokeHandler(message, item, args, kwargs)
        
    @staticmethod
    def add(member_id: int, title: str, items: dict[str, Any], complete_handler: EventHandler | None = None, error_handler: EventHandler | None = None, args: list = [], kwargs: dict = {}):
        search_complete_handler = EventHandler(coro_event=Search.__search_complete_handler)
        def checker(message: disnake.Message):
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
                
        Ask.add(member_id, search_complete_handler, error_handler, checker, [items] + [complete_handler] + args, kwargs)
        return Embed(
            title=title,
            description='\n'.join([f'**{i + 1}.** {item}' for i, item in enumerate(items.keys())]),
            colour=Colour.green()
        )


deps.bot.add_cog(Ask())