import dependencies as deps
import config

config.first_config()

@deps.bot.event
async def on_ready():
    await config.second_config()

if __name__ == "__main__":
    deps.bot.run(deps.TOKEN)

# Сделано с любовью группой EGR
# Если вы читаете этот комментарий, значит вы в далеком будущем и Егрей будущего бподелился с вами этим кодом. В таком случае Егрей прошлого передает вам счастья и успехов!