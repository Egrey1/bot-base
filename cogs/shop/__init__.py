from .commands import *

class ShopCog(InvCommand, ShopCommand, BuyCommand, SellItem):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(ShopCog(bot))