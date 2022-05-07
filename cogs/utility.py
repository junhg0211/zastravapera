from datetime import datetime
from random import choice, randint

import requests
from discord import Embed, utils
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from discord_slash import cog_ext, SlashContext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from sat_datetime import SatDatetime

from const import get_const
from util import get_programwide, jwiki
from util.thravelemeh import WordGenerator

guild_ids = get_programwide('guild_ids')


class UtilityCog(Cog):
    def __init__(self, bot: Bot):
        self.main_channel = utils.get(bot.get_all_channels(), id=get_const('main_channel_id'))

        self.last_recent_changes = datetime.now()

        self.track_recent_changes.start()

    @tasks.loop(seconds=600)
    async def track_recent_changes(self):
        changes = jwiki.get_recent_changes(from_=self.last_recent_changes)

        embed = Embed(title='최근 변경된 문서', description=str(self.last_recent_changes), color=get_const('sat_color'))

        if 'item' in changes:
            changes = changes['item']
            for change in changes:
                if '사트' in jwiki.get_categories(change['title']):
                    embed.add_field(
                        name=change['title'],
                        value=f'[{change["pubDate"]}]({change["link"]})'
                    )
            await self.main_channel.send(embed=embed)
        else:
            await self.main_channel.send(
                f'최근 변경된 문서가 없습니다. 제이위키 `[[분류:사트]]` 문서에 변경 사항이 발생되면 알려드리겠습니다. '
                f'이 메시지는 1분 후에 삭제됩니다.\n'
                f'> {self.last_recent_changes}', delete_after=60)
        self.last_recent_changes = datetime.now()

    @cog_ext.cog_slash(
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
    async def word(self, ctx: SlashContext, consonants: str, vowels: str, syllables: str, count: int = 10):
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
            words.append(f'{i + 1}. ')
            syllable = choice(syllables)
            for character in syllable:
                words[-1] += choice(consonants) if character == 'c' else choice(vowels)

        embed = Embed(
            title='랜덤 생성 단어',
            description=', '.join(syllables),
            color=get_const('shtelo_sch_vanilla')
        )
        embed.add_field(name='단어 목록', value='\n'.join(words))

        await message.edit(embed=embed, content='')

    @cog_ext.cog_slash(
        name='thword',
        guild_ids=guild_ids,
        description='랜덤한 트라벨레메 단어를 만들어줍니다.'
    )
    async def thword(self, ctx: SlashContext):
        message = await ctx.send('단어 생성중입니다...')

        generator = WordGenerator()
        words = generator.generate_words()

        embed = Embed(
            title='랜덤 트라벨레메 단어',
            color=get_const('hemelvaarht_hx_nerhgh')
        )
        embed.add_field(name='단어 목록', value='\n'.join(words))

        await message.edit(embed=embed, content='')

    @cog_ext.cog_slash(
        description='주사위를 굴립니다.',
        options=[
            create_option(
                name='kind',
                description='주사위의 종류를 정합니다. (d4, d6, d8, d10, d12, d20, d100, d%) 등을 사용할 수 있습니다.',
                option_type=3,
                choices=['d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100', 'd%'],
                required=False
            ),
            create_option(
                name='count',
                description='굴리는 주사위의 개수',
                option_type=4,
                required=False
            )
        ]
    )
    async def dice(self, ctx: SlashContext, kind: str = 'd6', count: int = 1):
        if kind == 'd%':
            kind = 'd100'
        kind = int(kind[1:])

        dice = 0
        numbers = list()
        for _ in range(count):
            number = randint(1, kind)
            dice += number
            numbers.append(number)

        embed = Embed(
            title='주사위 굴림',
            description=f'{count}d{kind}'
        )
        embed.add_field(name='굴린 주사위', value=', '.join(map(str, numbers)))
        embed.add_field(name='눈 합', value=str(dice))

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        description='계산 기능을 수행합니다.',
        options=[
            create_option(
                name='operation',
                description='수식을 입력합니다. (예: 1 + 2)',
                option_type=3,
                required=True
            )
        ]
    )
    async def calc(self, ctx: SlashContext, operation: str):
        for letter in operation:
            if letter not in '0123456789+-*/^(). ':
                await ctx.send('잘못된 수식입니다.')
                return

        # noinspection PyBroadException
        try:
            result = eval(operation)
        except Exception:
            await ctx.send('잘못된 수식입니다.')
            return
        else:
            await ctx.send(f'`{operation} =` __{result}__')

    @cog_ext.cog_slash(
        description='자소크력을 계산합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='year',
                description='자소크력을 계산할 년도를 입력합니다.',
                option_type=4,
                required=False
            ),
            create_option(
                name='month',
                description='자소크력을 계산할 월을 입력합니다.',
                option_type=4,
                required=False
            ),
            create_option(
                name='day',
                description='자소크력을 계산할 일을 입력합니다.',
                option_type=4,
                required=False
            ),
            create_option(
                name='hour',
                description='자소크력을 계산할 시간을 입력합니다.',
                option_type=4,
                required=False
            ),
            create_option(
                name='minute',
                description='자소크력을 계산할 분을 입력합니다.',
                option_type=4,
                required=False
            ),
            create_option(
                name='second',
                description='자소크력을 계산할 초를 입력합니다.',
                option_type=10,
                required=False
            ),
        ]
    )
    async def zacalen(self, ctx: SlashContext, year: int = 0, month: int = 0, day: int = 0,
                      hour: int = 0, minute: int = 0, second: float = 0.0):
        now = datetime.now()
        now = datetime(
            year if year else now.year,
            month if month else now.month,
            day if day else now.day,
            hour if hour else now.hour,
            minute if minute else now.minute,
            second if second else now.second
        )
        sat_datetime = SatDatetime.get_from_datetime(now)
        await ctx.send(f'> 서력 {now.year}년 {now.month}월 {now.day}일 {now.hour}시 {now.minute}분 {now.second}초는\n'
                       f'> 자소크력은 __{sat_datetime.year}년 {sat_datetime.month}월 {sat_datetime.day}일 '
                       f'{sat_datetime.hour}시 {sat_datetime.minute}분 {sat_datetime.second:.1f}초__ 입니다.')

    @cog_ext.cog_slash(
        description='제이위키 문서릅 검색합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='query',
                description='검색어를 입력합니다.',
                option_type=SlashCommandOptionType.STRING,
                required=True
            )
        ]
    )
    async def jwiki(self, ctx: SlashContext, query: str):
        response = requests.get(f'https://jwiki.kr/wiki/api.php?action=query&list=search&srsearch={query}&format=json')
        if response.status_code != 200:
            await ctx.send('제이위키 문서 검색에 실패했습니다.')
            return
        data = response.json()
        if 'query' not in data or 'search' not in data['query']:
            await ctx.send('제이위키 문서 검색에 실패했습니다.')
            return
        if not data['query']['search']:
            await ctx.send('검색 결과가 없습니다.')
            return

        embed = Embed(title=f'`{query}` 제이위키 문서 검색 결과', color=get_const('jwiki_color'))
        for result in data['query']['search'][:25]:
            embed.add_field(
                name=result['title'],
                value=f'[보러 가기](https://jwiki.kr/wiki/index.php/{result["title"].replace(" ", "_")})',
                inline=False)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(UtilityCog(bot))
