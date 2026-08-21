from disnake.ext.commands import Cog, command, Context
from disnake.ext import tasks
from disnake import Member, Embed, Colour, Message, User, MessageInteraction, TextInputStyle, ModalInteraction, MediaGalleryItem, MessageFlags
from disnake.ui import Button, View
import disnake.ui as ui

import dependencies as deps
import asyncio
from typing import Tuple