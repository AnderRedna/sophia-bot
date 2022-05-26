""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

from disnake.ext import commands
from disnake.ext.commands import Context
import disnake
import time

from helpers import checks


class Template(commands.Cog, name="template-normal"):
    def __init__(self, bot):
        self.bot = bot

#(Comando: !falar <menssagem>)
    @commands.command(
        name="fale",
        description="A Sophia vai falar o que você digitar no canal que você escolher!",
    )
    @checks.not_blacklisted()

    @checks.is_owner()
    async def fale(ctx, self, channel: int, message2: str):
        channel = self.bot.get_channel(channel)
        await channel.send(message2)

#(Comando: !falar <menssagem>)
    @commands.command(
        name="falar",
        description="A Sophia vai falar o que você digitar no canal que você escolher!",
    )
    @checks.not_blacklisted()

    @checks.is_owner()
    async def falar(self, context: Context, *, message: str):
        print(message)
        await context.send(message)

#(Comando: !audio <id da sala> <nome da musica>)
    @commands.command(
        name="audio",
        description="A Sophia vai falar no canal que você escolher!",
    )
    @checks.not_blacklisted()

    @checks.is_owner()
    async def audio(ctx, self, message1: int, message2: str):
        channel = self.bot.get_channel(message1)
        voice = await channel.connect()
        voice.play(disnake.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=("audios/" + message2 + ".mp3")))
        time.sleep(4)
        await self.guild.voice_client.disconnect()

def setup(bot):
    bot.add_cog(Template(bot))
