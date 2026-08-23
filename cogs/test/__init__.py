import disnake
from disnake.ext import commands
import dependencies as deps

class Test(commands.Cog):
    async def complete_handler(self, message: disnake.Message, item: str, args: list, kwargs: dict):
        await message.channel.send(f'Вы выбрали элемент: {item}\n{args}, {kwargs}')
    
    async def error_handler(self, message: disnake.Message, embed: disnake.Embed, *args, **kwargs):
        await message.channel.send(embed=embed)
        
    @commands.command(name='test', description='Тестовая команда')
    async def test_command(self, ctx: commands.Context):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
            'g': 7
        }
        complete = deps.EventHandler(coro_event=self.complete_handler)
        error = deps.EventHandler(coro_event=self.error_handler)
        await ctx.send(embed=deps.Search.add(ctx.author.id, 'Выберите элемент', d, complete_handler=complete, error_handler=error, args=[1, 2, 3], kwargs={'a': 1, 'b': 2}))
        
def setup(bot):
    bot.add_cog(Test())