from .commands import *

class MainCommands(Test, VersionCommand):
    pass

def setup(bot):
    bot.add_cog(MainCommands())