import dependencies as deps
import config

config.first_config()

@deps.bot.event
async def on_ready():
    await config.second_config()

if __name__ == "__main__":
    deps.bot.run(deps.TOKEN)

# Сделано с любовью группой EGR

# Этот код это база для всех наших ботов в дискорде. Можете ознакомиться