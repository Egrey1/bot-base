bot: Bot
intents: Intents
PREFIX: tuple[str]
TOKEN: str
VERSION: str
test_mode: bool

class Search:
    def __init__(self, label: str, items: dict[str, Any], member_id: int, complete_handler: 'EventHandler | None' = None, error_handler: 'EventHandler | None' = None) :
        """
        Создание объекта поиска

        Params:
            label (str): **Оглавление списка предметов для поиска**
            items (dict[str, Any]): **Словарь предметов для поиска. Ключ это название предмета, значение - сам предмет**
            member_id (int): **ID пользователя, который ищет предметы**
            complete_handler: **Обработчик события, когда поиск завершается удачно. В качестве аргумента обработчик принимает объект типа Message, выбранный предмет и ID участника**
            error_handler: **Обработчик события, когда поиск завершается неудачно. В качестве аргумента обработчик принимает объект типа Message, Embed и int. Сообщение, к которому привязана ошибка, его описание и ID участника**
        """
    
    async def send_label(self, ctx: Context):
        """
        Отправить окно с предметами

        Params:
            ctx (Context): **Контекст сообщения**
        """
    
    async def on_message_handler(self, message: Message):
        """
        Вся проверка и суть поиска. Вызывать строго в обработчике сообщений on_message
        """

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