from asyncio import sleep
from copy import copy
from datetime import datetime, timedelta
from random import choice, randint
from typing import Optional, Dict, List
from urllib import parse

import requests
from discord import Embed, TextChannel
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from discord_slash import cog_ext, SlashContext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from sat_datetime import SatDatetime, SatTimedelta

from const import get_const, get_secret
from util import get_programwide, jwiki
from util.thravelemeh import WordGenerator

RECENT_CHANGE_DURATION = 10 * 60

guild_ids = get_programwide('guild_ids')


def create_convert_table():
    pipere_rome = 'ABCDEFGHIKLMNOPQRSTVUZ'
    pipere_gree = 'ΑΒΨΔΕΦΓΗΙΚΛΜΝΟΠϞΡΣΤѶΥΖ'

    result = {'OO': 'Ω', '-': '⳼'}
    result.update({r: g for r, g in zip(pipere_rome, pipere_gree)})
    for k, v in copy(result).items():
        result[k.lower()] = v.lower()

    return result


def lumiere_number(arabic):
    number_define = ['za', 'ho', 'san', 'ni', 'chi', 'la', 'pi', 'kan', 'kain', 'laio']
    result = ''
        
    for number in str(arabic):
        result += number_define[int(number)]
    
    return result


PIPERE_CONVERT_TABLE = create_convert_table()


class UtilityCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        self.main_channel: Optional[TextChannel] = None

        self.last_recent_changes = datetime.now()
        self.track_recent_changes.start()

    def cog_unload(self):
        pass

    # noinspection PyTypeChecker
    async def recent_changes(self, ctx: Optional[SlashContext], channel: TextChannel):
        if ctx is not None:
            send = ctx.send
        else:
            send = channel.send

        changes = jwiki.get_recent_changes(from_=self.last_recent_changes)['rss']['channel']

        result: Dict[str, List[int, int, str]] = dict()
        if 'item' in changes:
            changes = changes['item']
            if isinstance(changes, dict):
                changes = [changes]
            for change in changes:
                await sleep(0)
                # merge duplicated changes
                parsed = parse.parse_qs(parse.urlsplit(change['link']).query)
                if 'title' in parsed:
                    title = parsed['title'][0]
                    diff = int(parsed['diff'][0])
                    oldid = int(parsed['oldid'][0])
                    if title in result:
                        original_oldid = int(result[title][0])
                        original_diff = int(result[title][1])
                        result[title][0] = min(original_oldid, oldid)
                        result[title][1] = max(original_diff, diff)
                    else:
                        result[title] = [oldid, diff, change['dc:creator']]

        if result:
            embed = Embed(
                title='최근 변경된 문서', description=f'{self.last_recent_changes}부터',
                color=get_const('sat_color'))
            for title, (oldid, diff, creator) in result.items():
                embed.add_field(
                    name=title.replace('_', ' '),
                    value=f'`{creator}`님이 마지막으로 [수정](https://jwiki.kr/wiki/index.php?'
                          f'title={title.replace(" ", "_")}&oldid={oldid}&diff={diff})함.'
                )
            await send(embed=embed)

        self.last_recent_changes = datetime.now()

    @tasks.loop(seconds=10)
    async def track_recent_changes(self):
        """ 광부위키 최근 변경 사항을 채팅 채널에 전송합니다. """

        if datetime.now() - self.last_recent_changes < timedelta(seconds=RECENT_CHANGE_DURATION):
            return

        while self.main_channel is None:
            self.main_channel = self.bot.get_channel(get_const('changes_channel_id'))
            await sleep(1)

        await self.recent_changes(None, self.main_channel)

    @cog_ext.cog_slash(
        name='recent',
        description='최근 발생한 사트 변경 사항을 채팅 채널에 전송합니다.',
        guild_ids=guild_ids
    )
    async def recent(self, ctx: SlashContext):
        """ 최근 발생한 사트 변경 사항을 채팅 채널에 전송합니다. """

        await self.recent_changes(ctx, ctx.channel)

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
        await ctx.send(f'> 서력 {now.year}년 {now.month}월 {now.day}일 {now.hour}시 {now.minute}분 {now.second}초 (UTC)는\n'
                       f'> 자소크력으로 __{sat_datetime.year}년 {sat_datetime.month}월 {sat_datetime.day}일 '
                       f'{sat_datetime.hour}시 {sat_datetime.minute}분 {sat_datetime.second:.1f}초 (ASN)__ 입니다.')

    @cog_ext.cog_slash(
        description='코르력을 계산합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='year',
                description='코르력을 계산할 년도를 입력합니다.',
                option_type=4,
                required=False
            ),
            create_option(
                name='month',
                description='코르력을 계산할 월을 입력합니다.',
                option_type=4,
                required=False
            ),
            create_option(
                name='day',
                description='코르력을 계산할 일을 입력합니다.',
                option_type=4,
                required=False
            ),
            create_option(
                name='hour',
                description='코르력을 계산할 시간을 입력합니다.',
                option_type=4,
                required=False
            ),
            create_option(
                name='minute',
                description='코르력을 계산할 분을 입력합니다.',
                option_type=4,
                required=False
            ),
            create_option(
                name='second',
                description='코르력을 계산할 초를 입력합니다.',
                option_type=10,
                required=False
            ),
        ]
    )
    async def khorcalen(self, ctx: SlashContext, year: int = 0, month: int = 0, day: int = 0,
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
        sat_datetime = SatDatetime.get_from_datetime(now) - SatTimedelta(years=3276)
        await ctx.send(f'> 서력 {now.year}년 {now.month}월 {now.day}일 {now.hour}시 {now.minute}분 {now.second}초 (UTC)는\n'
                       f'> 코르력으로 __{sat_datetime.year}년 {sat_datetime.month}월 {sat_datetime.day}일 '
                       f'{sat_datetime.hour}시 {sat_datetime.minute}분 {sat_datetime.second:.1f}초 (ASN)__ 입니다.')

    @cog_ext.cog_slash(
        description='자소크력으로 서력 일자를 계산합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='year',
                description='자소크력 년',
                option_type=SlashCommandOptionType.INTEGER,
                required=True
            ),
            create_option(
                name='month',
                description='자소크력 월',
                option_type=SlashCommandOptionType.INTEGER,
                required=False
            ),
            create_option(
                name='day',
                description='자소크력 일',
                option_type=SlashCommandOptionType.INTEGER,
                required=False
            )
        ]
    )
    async def inzacalen(self, ctx: SlashContext, year: int, month: int = 1, day: int = 1):
        sat_datetime = SatDatetime(year, month, day)
        christian_era = sat_datetime.to_datetime()
        await ctx.send(f'> 자소크력 {year}년 {month}월 {day}일 (ASN)은\n'
                       f'> 서력 __{christian_era.year}년 {christian_era.month}월 {christian_era.day}일 {christian_era.hour}시 '
                       f'{christian_era.minute}분 {christian_era.second:.1f}초 (UTC)__입니다.')
        
    @cog_ext.cog_slash(
        description='코르력으로 서력 일자를 계산합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='year',
                description='코르력 년',
                option_type=SlashCommandOptionType.INTEGER,
                required=True
            ),
            create_option(
                name='month',
                description='코르력 월',
                option_type=SlashCommandOptionType.INTEGER,
                required=False
            ),
            create_option(
                name='day',
                description='코르력 일',
                option_type=SlashCommandOptionType.INTEGER,
                required=False
            )
        ]
    )
    async def inkhorcalen(self, ctx: SlashContext, year: int, month: int = 1, day: int = 1):
        sat_datetime = SatDatetime(year, month, day) + SatTimedelta(years=3276)
        christian_era = sat_datetime.to_datetime()
        await ctx.send(f'> 코르력 {year}년 {month}월 {day}일 (ASN)은\n'
                       f'> 서력 __{christian_era.year}년 {christian_era.month}월 {christian_era.day}일 {christian_era.hour}시 '
                       f'{christian_era.minute}분 {christian_era.second:.1f}초 (UTC)__입니다.')

    @cog_ext.cog_slash(
        description='광부위키 문서릅 검색합니다.',
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
    async def gwangbu(self, ctx: SlashContext, query: str):
        response = requests.get(f'http://wiki.shtelo.org/api.php?action=query&list=search&srsearch={query}&format=json')
        if response.status_code != 200:
            await ctx.send('광부위키 문서 검색에 실패했습니다.')
            return
        data = response.json()
        if 'query' not in data or 'search' not in data['query']:
            await ctx.send('광부위키 문서 검색에 실패했습니다.')
            return
        if not data['query']['search']:
            await ctx.send('검색 결과가 없습니다.')
            return

        embed = Embed(title=f'`{query}` 광부위키 문서 검색 결과', color=get_const('sat_color'))
        for result in data['query']['search'][:25]:
            embed.add_field(
                name=result['title'],
                value=f'[보러 가기](http://wiki.shtelo.org/index.php/{result["title"].replace(" ", "_")})',
                inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        description='여론조사를 실시합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='title',
                description='여론조사 제목을 입력합니다.',
                option_type=SlashCommandOptionType.STRING,
                required=True
            ),
            create_option(
                name='content',
                description='여론조사 내용을 입력합니다.',
                option_type=SlashCommandOptionType.STRING,
                required=True
            ),
            create_option(
                name='answer_count',
                description='여론조사 정답의 개수를 입력합니다.',
                option_type=SlashCommandOptionType.INTEGER,
                required=True
            )
        ]
    )
    async def poll(self, ctx: SlashContext, title: str, content: str, answer_count: int):
        if answer_count < 2:
            await ctx.send('정답의 개수는 2개 이상이어야 합니다.')
            return
        elif answer_count > 20:
            await ctx.send('정답의 개수는 20개 이하이어야 합니다.')
            return

        message = await ctx.send(f'**{title}**\n> {content}')
        for i in range(answer_count):
            await message.add_reaction(chr(ord('🇦') + i))
            await sleep(0)

    @cog_ext.cog_slash(
        description='한국어 단어를 검색합니다.',
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
    async def korean(self, ctx: SlashContext, query: str):
        message = await ctx.send(f'표준국어대사전에서 `{query}` 단어를 검색하는 중입니다…')

        r = requests.get('https://stdict.korean.go.kr/api/search.do',
                         params={'key': get_secret('korean_dictionary_api_key'), 'q': query, 'req_type': 'json'},
                         verify=False)
        try:
            j = r.json()
        except requests.exceptions.JSONDecodeError:
            await message.edit(content=f'`{query}`의 검색결과가 없습니다.')
            return
        else:
            words = j['channel']['item']

            embed = Embed(title=f'`{query}` 한국어 사전 검색 결과', color=get_const('korean_color'),
                          description='출처: 국립국어원 표준국어대사전')
            for word in words:
                embed.add_field(name=f"**{word['word']}** ({word['pos']})",
                                value=word['sense']['definition'] + f' [자세히 보기]({word["sense"]["link"]})',
                                inline=False)

            await message.edit(content=None, embed=embed)

    @cog_ext.cog_slash(
        description='피페레어 변환기를 실행합니다',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='roman',
                description='로마자 문자열을 입력합니다.',
                option_type=SlashCommandOptionType.STRING,
                required=True
            )
        ]
    )
    async def pipeconv(self, ctx: SlashContext, roman: str):
        for k, v in PIPERE_CONVERT_TABLE.items():
            roman = roman.replace(k, v)

        await ctx.send(f'변환 결과:\n> {roman}')

    @cog_ext.cog_slash(
        description='뤼미에르 숫자로 변환합니다.',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='arabic',
                description='아라비아 숫자를 입력합니다.',
                option_type=SlashCommandOptionType.INTEGER,
                required=True
            )
        ]
    )
    async def luminum(self, ctx: SlashContext, arabic: int):
        result = lumiere_number(arabic)
        await ctx.send(f'> **아라비아 숫자** : {arabic}\n> **뤼미에르 숫자** : {result}')


def setup(bot: Bot):
    bot.add_cog(UtilityCog(bot))
