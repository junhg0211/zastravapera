import random
from os import listdir

from discord import Embed
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

from const import get_secret, get_const
from util import set_programwide
from util.thravelemeh import WordGenerator

bot = Bot(command_prefix='$$', self_bot=True)
slash = SlashCommand(bot, sync_commands=True)

guild_ids = set_programwide('guild_ids', list())


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

    await message.edit(embed=embed, content='')


@slash.slash(
    name='thword',
    guild_ids=guild_ids,
    description='랜덤한 트라벨레메 단어를 만들어줍니다.'
)
async def thword(ctx: SlashContext):
    message = await ctx.send('단어 생성중입니다...')

    generator = WordGenerator()
    words = generator.generate_words()

    embed = Embed(
        title='랜덤 트라벨레메 단어',
        color=get_const('hemelvaarht_hx_nerhgh')
    )
    embed.add_field(name='단어 목록', value='\n'.join(words))

    await message.edit(embed=embed, content='')


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
