from discord import Embed
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

from const import get_secret, get_const
from database import Database, ThravelemehWord, ZasokeseWord, BerquamWord

bot = Bot(command_prefix='$$')
slash = SlashCommand(bot, sync_commands=True)
databases = {
    'zasokese': Database(ZasokeseWord, 'zasokese_database'),
    'thravelemeh': Database(ThravelemehWord, 'thravelemeh_database'),
    'berquam': Database(BerquamWord, 'zasokese_database', 1)
}


async def handle_dictionary(ctx: SlashContext, database: Database, embed: Embed, query: str):
    message = await ctx.send(f'`{query}`에 대해 검색 중입니다…')

    words, duplicates, reloaded = database.search_rows(query)
    if len(words) > 25:
        await ctx.send(content='검색 결과가 너무 많습니다. 좀 더 자세히 검색해주세요.')
        return

    tmp = 0
    while duplicates and words:
        word = words.pop(duplicates.pop() - tmp)
        word.add_to_field(embed, True)
        tmp += 1
    for word in words:
        word.add_to_field(embed)
    if not words and not tmp:
        embed.add_field(name='검색 결과', value='검색 결과가 없습니다.')

    await message.edit(content='데이터베이스를 다시 불러왔습니다.' if reloaded else '', embed=embed)


@slash.slash(
    name='zasok',
    description='자소크어 단어를 검색합니다.',
    guild_ids=get_const('guild_ids'),
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
    await handle_dictionary(ctx, databases['zasokese'], Embed(
        title=f'`{query}`의 검색 결과',
        description='자소크어 단어를 검색합니다.',
        color=get_const('shtelo_sch_vanilla')
    ), query)


@slash.slash(
    name='th',
    description='트라벨레메 단어를 검색합니다.',
    guild_ids=get_const('guild_ids'),
    options=[
        create_option(
            name='query',
            description='검색할 단어',
            required=True,
            option_type=3
        )
    ]
)
async def th(ctx: SlashContext, query: str):
    await handle_dictionary(ctx, databases['thravelemeh'], Embed(
        title=f'`{query}`의 검색 결과',
        description='트라벨레메 단어를 검색합니다.',
        color=get_const('hemelvaarht_hx_nerhgh')
    ), query)


@slash.slash(
    name='berquam',
    description='베르쿠암 단어를 검색합니다.',
    guild_ids=get_const('guild_ids'),
    options=[
        create_option(
            name='query',
            description='검색할 단어',
            required=True,
            option_type=3
        )
    ]
)
async def berquam(ctx: SlashContext, query: str):
    await handle_dictionary(ctx, databases['berquam'], Embed(
        title=f'`{query}`의 검색 결과',
        description='베르쿠암 단어를 검색합니다.',
        color=get_const('berquam_color')
    ), query)


@slash.slash(
    name='reload',
    description='데이터베이스를 다시 불러옵니다.',
    guild_ids=get_const('guild_ids')
)
async def reload(ctx: SlashContext):
    message = await ctx.send('데이터베이스를 다시 불러옵니다…')
    for database in databases.values():
        database.reload()
    await message.edit(content='데이터베이스를 다시 불러왔습니다.')


bot.run(get_secret('bot_token'))
