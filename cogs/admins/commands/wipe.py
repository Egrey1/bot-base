from ..library import Cog, Context, deps, command, Embed, Colour

class Wipe(Cog):
    @command('wipe')
    async def wipe(self, ctx: Context):
        if ctx.author.id != (ctx.guild.owner_id or 0):
            return await ctx.send(embed=Embed(
                title='Ошибка',
                description='Эту команду может запустить только владелец сервера',
                color=Colour.red()
            ))
        try:
            with deps.main_db as connect:
                cursor = connect.cursor()
                for table in ('user_inventory', 'user_balances', 'shop_items'):
                    cursor.execute(f"""
                        DELETE FROM {table}
                    """)
                    connect.commit()
                await ctx.send(embed=Embed(
                    title='Успешно',
                    description='БД вайпа была успешно почищена',
                    color=Colour.green()
                ))
        except:
            await ctx.send(embed=Embed(
                title='Ошибка',
                description='Была вызвана неизвестная ошибка',
                color=Colour.red()
            ))