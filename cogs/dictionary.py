from asyncio import sleep, TimeoutError as AsyncTimeoutError

from discord import Embed
from discord.ext.commands import Cog, Bot
from discord_slash import SlashContext, cog_ext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from const import get_const
from database import Database, DialectDatabase, PosDatabase, SimpleDatabase
from database.arteut import ArteutWord
from database.enjie import EnjieDatabase
from database.felinkia import FelinkiaWord
from database.hemelvaarht import ThravelemehWord
from database.iremna import IremnaWord
from database.mikhoros import MikhorosWord
from database.sesame import SesameWord
from database.zasok import ZasokeseWord, BerquamWord
from database.fsovm import FsovmWord
from util import get_programwide
from util.simetasis import zasokese_to_simetasise

databases = {
    'zasokese': Database(ZasokeseWord, 'zasokese_database'),
    'thravelemeh': Database(ThravelemehWord, 'thravelemeh_database'),
    'berquam': Database(BerquamWord, 'zasokese_database', 1),
    'simetasispika': DialectDatabase(ZasokeseWord, 'zasokese_database', zasokese_to_simetasise),
    'felinkia': Database(FelinkiaWord, 'felinkia_database'),
    '4351': Database(SesameWord, '4351_database', 0),
    'semal': PosDatabase('semal_database'),
    'xei': PosDatabase('xei_database', 0, 0, 2, 3),
    'iremna': Database(IremnaWord, 'iremna_database', 0),
    'arteut': Database(ArteutWord, 'arteut_database', 0),
    'enjie': EnjieDatabase('enjie_database'),
    'mikhoros': Database(MikhorosWord, 'mikhoros_database'),
    'pain': SimpleDatabase('liki_database'),
    'fsovm': Database(FsovmWord, 'fsovm_database')
}

guild_ids = get_programwide('guild_ids')


async def handle_dictionary(ctx: SlashContext, database: Database, embed: Embed, query: str):
    """
    Handles the dictionary command.

    :param ctx:
    :param database:
    :param embed:
    :param query: 검색어
    """
    message = await ctx.send(f'`{query}`에 대해 검색 중입니다…')

    words, duplicates, reloaded = database.search_rows(query)
    too_many = False
    if (word_count := len(words)) > 25:
        too_many = True
        words = list(map(lambda x: words[x], duplicates))
        duplicates = set()

    index_offset = 0
    while duplicates and words:
        word = words.pop(duplicates.pop() - index_offset)
        word.add_to_field(embed, True)
        index_offset += 1
    for word in words:
        word.add_to_field(embed)
    if not words and not index_offset:
        embed.add_field(name='검색 결과', value='검색 결과가 없습니다.')
    if too_many:
        embed.add_field(name='기타', value=f'단어나 뜻에 `{query}`가 들어가는 단어가 {word_count - index_offset} 개 더 있습니다.')

    await message.edit(content='데이터베이스를 다시 불러왔습니다.' if reloaded else '', embed=embed)


class DictionaryCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(
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
    async def zasok(self, ctx: SlashContext, query: str):
        if len(query) > 5:
            if any(query.startswith(prefix) for prefix in ('mò', 'mà', 'nò', 'nà', 'hò', 'hà', 'sò', 'sà')):
                query = query[2:]
            for character in 'àèìòù':
                if character in query:
                    index = query.index(character)
                    query = query[:index]

        await handle_dictionary(ctx, databases['zasokese'], Embed(
            title=f'`{query}`의 검색 결과',
            description='자소크어 단어를 검색합니다.',
            color=get_const('shtelo_sch_vanilla')
        ), query)

    @cog_ext.cog_slash(
        description='자소크어 단어를 만듭니다.',
        guild_ids=guild_ids,
        options=[
            create_option('word', '만들 단어', SlashCommandOptionType.STRING, True),
            create_option('origin_language', '어원 언어', SlashCommandOptionType.STRING, True),
            create_option('origin_word', '어원', SlashCommandOptionType.STRING, False),
            create_option('noun', '명사 의미', SlashCommandOptionType.STRING, False),
            create_option('adjective', '형용사 의미', SlashCommandOptionType.STRING, False),
            create_option('verb', '동사 의미', SlashCommandOptionType.STRING, False),
            create_option('adverb', '부사 의미', SlashCommandOptionType.STRING, False),
            create_option('postposition', '조사 의미', SlashCommandOptionType.STRING, False),
            create_option('note', '비고', SlashCommandOptionType.STRING, False),
        ]
    )
    async def zasok_create(self, ctx: SlashContext, word: str = '', origin_language: str = '', origin_word: str = '',
                           noun: str = '', adjective: str = '', verb: str = '', adverb: str = '',
                           postposition: str = '', note: str = ''):
        embed = Embed(title=f'자소크어 `{word}` 단어 추가', description='자소크어 단어를 추가합니다.',
                      color=get_const('shtelo_sch_vanilla'))
        embed.add_field(name='단어', value=word)
        if noun:
            embed.add_field(name='명사 의미', value=noun)
        if adjective:
            embed.add_field(name='형용사 의미', value=adjective)
        if verb:
            embed.add_field(name='동사 의미', value=verb)
        if adverb:
            embed.add_field(name='부사 의미', value=adverb)
        if postposition:
            embed.add_field(name='조사 의미', value=postposition)
        if note:
            embed.add_field(name='비고', value=note)
        if origin_language:
            embed.add_field(name='어원 언어', value=origin_language)
        if origin_word:
            embed.add_field(name='어원', value=origin_word)

        confirm = await ctx.send('추가하시겠습니까? (10초동안 대기)', embed=embed)
        await confirm.add_reaction('✅')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'
        try:
            await self.bot.wait_for('reaction_add', timeout=10, check=check)
        except AsyncTimeoutError:
            await confirm.remove_reaction('✅', self.bot.user)
            await confirm.edit(content='추가를 취소했습니다.')
            return

        databases['zasokese'] \
            .add_row([word, noun, adjective, verb, adverb, postposition, note, origin_language, origin_word])
        await confirm.edit(content='단어를 추가했습니다.')

    @cog_ext.cog_slash(
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
    async def th(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['thravelemeh'], Embed(
            title=f'`{query}`의 검색 결과',
            description='트라벨레메 단어를 검색합니다.',
            color=get_const('hemelvaarht_hx_nerhgh')
        ), query)

    @cog_ext.cog_slash(
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
    async def berquam(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['berquam'], Embed(
            title=f'`{query}`의 검색 결과',
            description='베르쿠암 단어를 검색합니다.',
            color=get_const('berquam_color')
        ), query)

    @cog_ext.cog_slash(
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
    async def sts(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['simetasispika'], Embed(
            title=f'`{query}`의 검색 결과',
            description='시메타시스어 단어를 검색합니다.',
            color=get_const('simetasis_color')
        ), query)

    @cog_ext.cog_slash(
        description='펠라인카이아어 단어를 검색합니다.',
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
    async def felinkia(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['felinkia'], Embed(
            title=f'`{query}`의 검색 결과',
            description='펠라인카이아어 단어를 검색합니다.',
            color=get_const('felinkia_color')
        ), query)

    @cog_ext.cog_slash(
        name='4351',
        description='4351 단어를 검색합니다.',
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
    async def sesame(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['4351'], Embed(
            title=f'`{query}`의 검색 결과',
            description='4351의 단어를 검색합니다.',
            color=get_const('4351_color')
        ), query)

    @cog_ext.cog_slash(
        name='semal',
        description='새말 단어를 검색합니다.',
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
    async def semal(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['semal'], Embed(
            title=f'`{query}`의 검색 결과',
            description='새말 단어를 검색합니다.',
            color=get_const('semal_color')
        ), query)

    @cog_ext.cog_slash(
        name='xei',
        description='헤이어 단어를 검색합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='query',
                description='검색할 단어',
                required=True,
                option_type=SlashCommandOptionType.STRING
            )
        ]
    )
    async def xei(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['xei'], Embed(
            title=f'`{query}`의 검색 결과',
            description='헤이어 단어를 검색합니다.',
            color=get_const('xei_color')
        ), query)

    @cog_ext.cog_slash(
        name='iremna',
        description='이렘나어 단어를 검색합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='query',
                description='검색할 단어',
                required=True,
                option_type=SlashCommandOptionType.STRING
            )
        ]
    )
    async def iremna(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['iremna'], Embed(
            title=f'`{query}`의 검색 결과',
            description='이렘나어 단어를 검색합니다.',
            color=get_const('iremna_color')
        ), query)

    @cog_ext.cog_slash(
        description='아르토이트어 단어를 검색합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='query',
                description='검색할 단어',
                required=True,
                option_type=SlashCommandOptionType.STRING
            )
        ]
    )
    async def arteut(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['arteut'], Embed(
            title=f'`{query}`의 검색 결과',
            description='아르토이트어 단어를 검색합니다.',
            color=get_const('arteut_color')
        ), query)

    @cog_ext.cog_slash(
        description='연서어 단어를 검색합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='query',
                description='검색할 단어',
                required=True,
                option_type=SlashCommandOptionType.STRING
            )
        ]
    )
    async def enjie(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['enjie'], Embed(
            title=f'`{query}`의 검색 결과',
            description='연서어 단어를 검색합니다.',
            color=get_const('enjie_color')
        ), query)

    @cog_ext.cog_slash(
        description='미코로스 아케뒤어 단어를 검색합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='query',
                description='검색할 단어',
                required=True,
                option_type=SlashCommandOptionType.STRING
            )
        ]
    )
    async def mikhoros(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['mikhoros'], Embed(
            title=f'`{query}`의 검색 결과',
            description='미코로스 아케뒤 단어를 검색합니다.',
            color=get_const('mikhoros_color')
        ), query)

    @cog_ext.cog_slash(
        description='파인어 단어를 검색합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='query',
                description='검색할 단어',
                required=True,
                option_type=SlashCommandOptionType.STRING
            )
        ]
    )
    async def pain(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['pain'], Embed(
            title=f'`{query}`의 검색 결과',
            description='파인어 단어를 검색합니다.',
            color=get_const('fliosen_color')
        ), query)

    @cog_ext.cog_slash(
        description='프소븜어 단어를 검색합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='query',
                description='검색할 단어',
                required=True,
                option_type=SlashCommandOptionType.STRING
            )
        ]
    )
    async def fsovm(self, ctx: SlashContext, query: str):
        await handle_dictionary(ctx, databases['fsovm'], Embed(
            title=f'`{query}`의 검색 결과',
            description='프소븜어 단어를 검색합니다.',
            color=get_const('tinudanma_color')
        ), query)

    @cog_ext.cog_slash(
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
    async def reload(self, ctx: SlashContext, language: str = ''):
        message = await ctx.send('데이터베이스를 다시 불러옵니다…')
        if language:
            if language not in databases:
                await message.edit(content='데이터베이스 이름을 확인해주세요!!')
                return

            databases[language].reload()
        else:
            for database in databases.values():
                database.reload()
                await sleep(0)
        await message.edit(content=f'{f"`{language}` " if language else ""}데이터베이스를 다시 불러왔습니다.')


def setup(bot: Bot):
    bot.add_cog(DictionaryCog(bot))
