from disnake.ext import commands
import dependencies as deps

class VersionCommand(commands.Cog):
    @commands.command('version')
    async def ver(self, ctx: commands.Context):
        await ctx.channel.send(deps.VERSION)