import random
from datetime import datetime

from discord import Embed
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

from const import get_secret, get_const
from database import Database, DialectDatabase
from database.hemelvaarht import ThravelemehWord
from database.zasok import ZasokeseWord, BerquamWord
from util import zasokese_to_simetasise

bot = Bot(command_prefix='$$')
slash = SlashCommand(bot, sync_commands=True)
databases = {'zasokese': Database(ZasokeseWord, 'zasokese_database'),
             'thravelemeh': Database(ThravelemehWord, 'thravelemeh_database'),
             'berquam': Database(BerquamWord, 'zasokese_database', 1),
             'simetasispika': DialectDatabase(ZasokeseWord, 'zasokese_database', zasokese_to_simetasise)}

guild_ids = list()


async def handle_dictionary(ctx: SlashContext, database: Database, embed: Embed, query: str):
    message = await ctx.send(f'`{query}`에 대해 검색 중입니다…')

    words, duplicates, reloaded = database.search_rows(query)
    if len(words) > 25:
        await message.edit(content='검색 결과가 너무 많습니다. 좀 더 자세히 검색해주세요.')
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


@bot.event
async def on_ready():
    global guild_ids

    guild_ids.clear()
    for guild_id in get_const('guild_ids'):
        guild = bot.get_guild(guild_id)
        if guild is not None:
            guild_ids.append(guild_id)
            print(f'Bot loaded on guild {guild.name}')

    print(f'Bot loaded. Bot is in {len(guild_ids)} guilds.')


@bot.event
async def on_command(ctx):
    now = datetime.now()
    print(f'{now} {ctx.guild.name} {ctx.author.name}#{ctx.author.discriminator}: {ctx.command.name}')


@slash.slash(
    name='zasok',
    description='자소크어 단어를 검색합니다.',
    guild_ids=guild_ids,
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
    guild_ids=guild_ids,
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
    guild_ids=guild_ids,
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
    name='sts',
    description='시메타시스 단어를 검색합니다.',
    guild_ids=guild_ids,
    options=[
        create_option(
            name='query',
            description='검색할 단어',
            required=True,
            option_type=3
        )
    ]
)
async def sts(ctx: SlashContext, query: str):
    await handle_dictionary(ctx, databases['simetasispika'], Embed(
        title=f'`{query}`의 검색 결과',
        description='시메타시스어 단어를 검색합니다.',
        color=get_const('simetasis_color')
    ), query)


@slash.slash(
    name='reload',
    description='데이터베이스를 다시 불러옵니다.',
    guild_ids=guild_ids,
    options=[
        create_option(
            name='language',
            description='데이터베이스를 불러올 언어를 설정합니다. 아무것도 입력하지 않으면 모든 언어의 데이터베이스를 다시 불러옵니다.',
            required=False,
            option_type=3,
            choices=list(databases.keys())
        )
    ]
)
async def reload(ctx: SlashContext, language: str = ''):
    message = await ctx.send('데이터베이스를 다시 불러옵니다…')
    if language:
        if language in databases:
            databases[language].reload()
        else:
            await message.edit(content='데이터베이스 이름을 확인해주세요!!')
    else:
        for database in databases.values():
            database.reload()
    await message.edit(content=f'{f"`{language}`" if language else ""}데이터베이스를 다시 불러왔습니다.')


@slash.slash(
    name='word',
    description='랜덤한 단어를 만들어줍니다.',
    options=[
        create_option(
            name='consonants',
            description='자음 목록 (콤마로 구분합니다.)',
            required=True,
            option_type=3
        ),
        create_option(
            name='vowels',
            description='모음 목록 (콤마로 구분합니다.)',
            required=True,
            option_type=3
        ),
        create_option(
            name='syllables',
            description='자음은 c, 모음은 v로 입력합니다. (대소문자 구분하지 않음, 콤마로 구분합니다.)',
            required=True,
            option_type=3
        ),
        create_option(
            name='count',
            description='만들 단어의 개수',
            required=False,
            option_type=4
        )
    ]
)
async def word(ctx: SlashContext, consonants: str, vowels: str, syllables: str, count: int = 10):
    syllables = syllables.lower()

    if syllables.replace('c', '').replace('v', '').replace(',', ''):
        await ctx.send('`syllables` 인자에는 `v`와 `c`만을 입력해주세요.')
        return

    syllables = syllables.split(',')

    message = await ctx.send('단어 생성중입니다...')

    consonants = consonants.split(',') if ',' in consonants else list(consonants)
    vowels = vowels.split(',') if ',' in vowels else list(vowels)

    words = list()
    for i in range(count):
        words.append(f'{i+1}. ')
        syllable = random.choice(syllables)
        for character in syllable:
            words[-1] += random.choice(consonants) if character == 'c' else random.choice(vowels)

    embed = Embed(
        title='랜덤 생성 단어',
        description=', '.join(syllables),
        color=get_const('shtelo_sch_vanilla')
    )
    embed.add_field(name='단어 목록', value='\n'.join(words))

    await message.edit(embed=embed)


if __name__ == '__main__':
    bot.run(get_secret('bot_token'))
