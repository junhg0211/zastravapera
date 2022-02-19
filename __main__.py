from discord import Embed
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

from const import get_secret, get_const
from database import Database

bot = Bot(command_prefix='$$')
slash = SlashCommand(bot, sync_commands=True)
database = Database()


@slash.slash(
    name='zasok',
    description='자소크어 단어를 검색합니다.',
    guild_ids=[561880172542820353],
    options=[
        create_option(
            name='query',
            description='검색할 단어',
            required=True,
            option_type=3
        )
    ]
)
async def zasok(ctx: SlashContext, query: str):
    embed = Embed(
        title=f'`{query}`의 검색 결과',
        description='자소크어 단어를 검색합니다.',
        color=get_const('shtelo_sch_vanilla')
    )
    words, duplicates, reloaded = database.search_rows(query)
    if len(words) > 25:
        await ctx.send(content='검색 결과가 너무 많습니다. 좀 더 자세히 검색해주세요.')
        return

    tmp = 0
    while duplicates:
        word = words.pop(duplicates.pop() - tmp)
        word.add_to_field(embed, True)
        tmp += 1
    for word in words:
        word.add_to_field(embed)
    if not words and not tmp:
        embed.add_field(name='검색 결과', value='검색 결과가 없습니다.')

    await ctx.send(content='데이터베이스를 다시 불러왔습니다.' if reloaded else '', embed=embed)


@slash.slash(
    name='reload',
    description='데이터베이스를 다시 불러옵니다.',
    guild_ids=[561880172542820353]
)
async def reload(ctx: SlashContext):
    database.reload()
    await ctx.send('데이터베이스를 다시 불러왔습니다.')


bot.run(get_secret('bot_token'))
