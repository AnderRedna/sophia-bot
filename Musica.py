from click import pass_context
import discord
from discord.ext import commands
import time
import asyncio
from disnake import FFmpegPCMAudio

from numpy import source

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="images/ara ara.mp3"))
        time.sleep(4)
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Não entrei no voice")

bot.run('OTc3NzQyNjU1NjQ1NjgzNzEy.G5eaF7.ZgT99IVGNCG6jT3z5B3GfLHYJgcRt9LYHk5gLg')