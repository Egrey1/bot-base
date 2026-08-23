from sqlite3 import Connection, connect, Row

interactive: Connection
"""
Временно без документации
"""

mute_db: Connection
"""
Временно без документации
"""

rights: Connection
"""
Подключение к SQLite-базе данных `rights.db`.

База данных используется для хранения прав ролей на пользование ботом.

Схема таблиц:
    `rights`
        Основная таблица. Формат записи всех полей: f'{Role.id};{Role.id}'...
        Поля:
            `manage_items TEXT`
                Право на управление предметами. Их редактирование, удаление и создание
            `manage_rincomes TEXT`
                Право на управление заработком ролей. Их редактирование, удаление и создание
            `manage_resources TEXT`
                Право на управление ресурсами. Их редактирование, удаление и создание
            `administrator TEXT`
                Все права выше и дополнительно позволяет назначать другие роли на другие права
"""

main_db: Connection
"""
Главное подключение к SQLite-базе данных `main.db`.

База данных используется как единое хранилище экономической системы бота.
В проекте предполагается работа только с одним Discord-сервером, поэтому
отдельная таблица серверов не используется.

Схема таблиц:
    `users`
        Хранит пользователей, которых уже видел бот.
        Поля:
            `id INTEGER PRIMARY KEY`
                Discord ID пользователя.
            `username TEXT`
                Имя пользователя на момент сохранения.
            `display_name TEXT`
                Отображаемое имя пользователя на момент сохранения.
            `created_at TEXT`
                Дата создания записи. Формат: `YYYY-MM-DD HH:MM:SS`.
            `updated_at TEXT`
                Дата последнего обновления записи. Формат: `YYYY-MM-DD HH:MM:SS`.

    `currencies`
        Хранит доступные валюты сервера.
        Поля:
            `id INTEGER PRIMARY KEY AUTOINCREMENT`
                Внутренний идентификатор валюты.
            `name TEXT UNIQUE`
                Уникальное имя валюты.
            `symbol TEXT`
                Символ валюты для отображения.
            `is_main INTEGER`
                Флаг основной валюты. Обычно `0` или `1`.
            `created_at TEXT`
                Время создания записи.
            `updated_at TEXT`
                Время последнего обновления записи.

    `resources`
        Хранит ресурсы, которые не являются валютой.
        Поля:
            `id INTEGER PRIMARY KEY AUTOINCREMENT`
                Внутренний идентификатор ресурса.
            `name TEXT UNIQUE`
                Уникальное имя ресурса.
            `description TEXT`
                Краткое описание ресурса.
            `emoji TEXT`
                Символ или emoji для отображения в сообщениях.
            `created_at TEXT`
                Время создания записи.
            `updated_at TEXT`
                Время последнего обновления записи.

    `user_balances`
        Хранит количество каждой валюты у каждого пользователя.
        Поля:
            `id INTEGER PRIMARY KEY AUTOINCREMENT`
                Идентификатор строки.
            `user_id INTEGER`
                Ссылка на `users.id`.
            `currency_id INTEGER`
                Ссылка на `currencies.id`.
            `amount INTEGER`
                Количество валюты у пользователя. Может быть как положительным, так и отрицательным.
            `bank INTEGER`
                Банковский баланс пользователя для этой валюты. Хранится отдельно от основного `amount`
                и не участвует в базовой логике экономики автоматически.
            `updated_at TEXT`
                Время последнего изменения значения.
        Формат хранения:
            одна строка = одна валюта у одного пользователя.

    `user_resources`
        Хранит количество каждого ресурса у каждого пользователя.
        Поля:
            `id INTEGER PRIMARY KEY AUTOINCREMENT`
                Идентификатор строки.
            `user_id INTEGER`
                Ссылка на `users.id`.
            `resource_id INTEGER`
                Ссылка на `resources.id`.
            `amount INTEGER`
                Количество ресурса у пользователя.
            `updated_at TEXT`
                Время последнего изменения значения.
        Формат хранения:
            одна строка = один ресурс у одного пользователя.

    `shop_items`
        Хранит предметы магазина.
        Поля:
            `id INTEGER PRIMARY KEY AUTOINCREMENT`
                Внутренний идентификатор предмета.
            `name TEXT UNIQUE`
                Название предмета.
            `description TEXT`
                Описание предмета.
            `cost_amount INTEGER`
                Цена предмета в выбранной валюте.
            `cost_currency_id INTEGER`
                Ссылка на `currencies.id`.
            `required_role_id INTEGER`
                Discord ID роли, необходимой для покупки. Может быть `NULL`.
            `stock INTEGER`
                Остаток предмета. `NULL` означает бесконечный запас.
            `is_active INTEGER`
                Флаг активности предмета. Обычно `0` или `1`.
            `tags TEXT`
                Список пользовательских тегов предмета в формате `tag;tag;tag`.
            `created_at TEXT`
                Время создания записи.
            `updated_at TEXT`
                Время последнего обновления записи.

    `user_inventory`
        Хранит предметы, принадлежащие пользователям.
        Поля:
            `id INTEGER PRIMARY KEY AUTOINCREMENT`
                Идентификатор строки.
            `user_id INTEGER`
                Ссылка на `users.id`.
            `shop_item_id INTEGER`
                Ссылка на `shop_items.id`.
            `amount INTEGER`
                Количество одинаковых предметов у пользователя.
            `updated_at TEXT`
                Время последнего изменения записи.
        Формат хранения:
            одна строка = один предмет магазина у одного пользователя.

    `role_incomes`
        Хранит роли, которые позволяют получать доход по кулдауну.
        Поля:
            `id INTEGER PRIMARY KEY AUTOINCREMENT`
                Внутренний идентификатор настройки дохода.
            `role_id INTEGER UNIQUE`
                Discord ID роли.
            `cooldown_seconds INTEGER`
                Кулдаун между сборами в секундах.
            `currency_id INTEGER`
                Ссылка на `currencies.id`. Может быть `NULL`, если роль не выдает валюту.
            `currency_amount REAL`
                Размер валютной награды. Может быть `NULL`, положительным, отрицательным или дробным.
            `is_active INTEGER`
                Флаг активности записи. Обычно `0` или `1`.
            `tags TEXT`
                Список пользовательских тегов доходной роли в формате `tag;tag;tag`.
            `created_at TEXT`
                Время создания записи.
            `updated_at TEXT`
                Время последнего обновления записи.

    `role_income_resources`
        Хранит ресурсы, которые дополнительно выдает доходная роль.
        Поля:
            `id INTEGER PRIMARY KEY AUTOINCREMENT`
                Идентификатор строки.
            `role_income_id INTEGER`
                Ссылка на `role_incomes.id`.
            `resource_id INTEGER`
                Ссылка на `resources.id`.
            `amount INTEGER`
                Количество ресурса за один сбор.
        Формат хранения:
            одна строка = один ресурс в награде одной роли.

    `role_income_claims`
        Хранит информацию о последнем сборе дохода пользователем.
        Поля:
            `id INTEGER PRIMARY KEY AUTOINCREMENT`
                Идентификатор строки.
            `role_income_id INTEGER`
                Ссылка на `role_incomes.id`.
            `user_id INTEGER`
                Ссылка на `users.id`.
            `last_claim_at TEXT`
                Момент последнего сбора в ISO-формате:
                `YYYY-MM-DDTHH:MM:SS` или `YYYY-MM-DDTHH:MM:SS.mmmmmm`.
        Формат хранения:
            одна строка = один пользователь для одной доходной роли.

Заметки:
    - Для работы с `main_db` проект использует `sqlite3.Row`, поэтому строки БД
      читаются по именам колонок.
    - При запуске проекта старые таблицы `role_incomes` и `user_balances`
      автоматически мигрируются, если в них еще остались ограничения,
      запрещающие отрицательные значения.
    - Объекты из `classes/objects/game_objects.py` уже знают, в какие таблицы
      обращаться, поэтому в основной логике чаще всего не нужен прямой SQL.
    - Для корректной работы связей в SQLite желательно включать
      `PRAGMA foreign_keys = ON`.
"""

interactive = connect('data/interactive.db', check_same_thread=False)
interactive.row_factory = Row
mute_db = connect('data/mutes.db', check_same_thread=False)
mute_db.row_factory = Row
rights = connect('data/rights.db', check_same_thread=False)
rights.row_factory = Row
rights.execute('PRAGMA foreign_keys = ON')
main_db = connect('data/main.db')