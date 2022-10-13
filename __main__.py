import re
from argparse import ArgumentParser
from os import listdir

from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand

from const import get_secret, get_const, override_const
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
    # noinspection PyProtectedMember
    parser._actions[0].help = '도움말 메시지를 보여주고 종료합니다'
    parser.add_argument('-t', '--test', action='store_true',
                        help='자스트라바페라 봇을 `test_bot_token`으로 실행합니다. '
                             '설정되지 않은 경우, `bot_token`으로 실행합니다')
    parser.add_argument('-c', '--cog', action='store', default=r'.*',
                        help='이 정규표현식을 만족하는 이름을 가진 코그만 실행합니다')
    parser.add_argument('-o', '--override', action='append',
                        help='const를 override합니다. `key=value`의 형태로 입력합니다.')

    args = parser.parse_args()

    if args.test:
        print('Run in test mode ...')

    if args.override:
        for override in args.override:
            key, value = override.split('=')
            override_const(key, eval(value))
            print(f'Constant overrode: {key} = {value}')

    load_cogs(args.cog)
    bot.run(get_secret('test_bot_token' if args.test else 'bot_token'))


if __name__ == '__main__':
    main()
