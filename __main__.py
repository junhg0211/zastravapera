import re
from argparse import ArgumentParser
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


def load_cogs(cog_re=r'.*'):
    filter_pattern = re.compile(cog_re)
    for file in listdir('cogs'):
        if file.endswith('.py') and not file.startswith('_'):
            if filter_pattern.search(file[:-3]) is None:
                continue

            cog_name = file[:-3]

            print(f'Loading cog `{cog_name}` ...', end='\r')
            bot.load_extension(f'cogs.{cog_name}')
            print(f'Cog loaded: {cog_name}      ')


def main():
    parser = ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true',
                        help='runs Zastravapera with `test_bot_token`. without, run with `bot_token` (res/secret.json)')
    parser.add_argument('-c', '--cog', action='store', default=r'.*',
                        help='runs Zastravapera whose name is searchable with this regex')

    args = parser.parse_args()

    if args.test:
        print('Run in test mode ...')

    load_cogs(args.cog)
    bot.run(get_secret('test_bot_token' if args.test else 'bot_token'))


if __name__ == '__main__':
    main()
