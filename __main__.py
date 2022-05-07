from os import listdir

from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand

from const import get_secret, get_const
from util import set_programwide

bot = Bot(command_prefix='$$', self_bot=True, intents=Intents.all())
slash = SlashCommand(bot, sync_commands=True)

guild_ids = set_programwide('guild_ids', list())


@bot.event
async def on_ready():
    guild_ids.clear()
    for guild_id in get_const('guild_ids'):
        guild = bot.get_guild(guild_id)
        if guild is not None:
            guild_ids.append(guild_id)
            print(f'Bot loaded on guild {guild.name}')

    print(f'Bot loaded. Bot is in {len(guild_ids)} guilds.')


for file in listdir('cogs'):
    if file.endswith('.py') and not file.startswith('_'):
        bot.load_extension(f'cogs.{file[:-3]}')
        print(f'Cog loaded: {file[:-3]}')


if __name__ == '__main__':
    bot.run(get_secret('bot_token'))
