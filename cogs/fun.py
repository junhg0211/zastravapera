from discord import Embed
from discord.ext.commands import Cog, Bot
from discord_slash import cog_ext, SlashCommandOptionType, SlashContext
from discord_slash.utils.manage_commands import create_option
import rsp

from util import get_programwide

guild_ids = get_programwide('guild_ids')


class FunCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(
        description="자스트라바페라와 가위바위보를 합니다.",
        guild_ids=guild_ids,
        options=[
            create_option(
                name='hand',
                description='낼 수를 입력합니다.',
                option_type=SlashCommandOptionType.STRING,
                required=True,
                choices=['가위', '바위', '보']
            )
        ]
    )
    async def rsp(self, ctx: SlashContext, hand: str):
        your_hand = rsp.hand_convert(hand)
        zastra_hand = rsp.random_choice()

        if rsp.is_a_winning_b(your_hand, zastra_hand):
            result = '승리'
        elif rsp.is_a_losing_b(your_hand, zastra_hand):
            result = '패배'
        else:
            result = '무승부'

        embed = Embed(title='가위바위보 세션', description=f'{ctx.author.mention} vs {self.bot.user.mention}')
        embed.add_field(name='당신의 수', value=rsp.stringify(your_hand))
        embed.add_field(name='자스트라바페라의 수', value=rsp.stringify(zastra_hand))
        embed.add_field(name='결과', value=f'**{result}**', inline=False)

        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(FunCog(bot))
