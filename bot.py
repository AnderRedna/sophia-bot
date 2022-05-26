import json
import os
import platform
import random
import sys
import time

from click import pass_context
from discord.ext import commands
import discord
import disnake
from disnake import ApplicationCommandInteraction, User
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context
from matplotlib.pyplot import eventplot

import exceptions

if not os.path.isfile("config.json"):
    sys.exit("'config.json' Não foi encontrado! Por favor adicione ele e continue.")
else:
    with open("config.json") as file:
        config = json.load(file)

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://docs.disnake.dev/en/latest/intents.html
https://docs.disnake.dev/en/latest/intents.html#privileged-intents


Default Intents:
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.messages = True # `message_content` is required to get the content of the messages
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True

Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
intents.members = True
intents.message_content = True
intents.presences = True
"""

intents = disnake.Intents.all()

intents.message_content = True

bot = Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents, help_command=None)
bot.config = config


@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logando como {bot.user.name}")
    print(f"Versão do disnake: {disnake.__version__}")
    print(f"Versão do Python: {platform.python_version()}")
    print(f"Rodando em: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot
    """
    statuses = ["Com você!", "League of legends (Estou perdendo)", "Com Humanos!"]
    await bot.change_presence(activity=disnake.Game(random.choice(statuses)))


def load_commands(command_type: str) -> None:
    for file in os.listdir(f"./cogs/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{command_type}.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


if __name__ == "__main__":
    """
    This will automatically load slash commands and normal commands located in their respective folder.
    
    If you want to remove slash commands, which is not recommended due to the Message Intent being a privileged intent, you can remove the loading of slash commands below.
    """
    load_commands("slash")
    load_commands("normal")


@bot.event
async def on_message(message: disnake.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix
    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_slash_command(interaction: ApplicationCommandInteraction) -> None:
    """
    The code in this event is executed every time a slash command has been *successfully* executed
    :param interaction: The slash command that has been executed.
    """
    print(
        f"Executed {interaction.data.name} command in {interaction.guild.name} (ID: {interaction.guild.id}) by {interaction.author} (ID: {interaction.author.id})")


@bot.event
async def on_slash_command_error(interaction: ApplicationCommandInteraction, error: Exception) -> None:
    """
    The code in this event is executed every time a valid slash command catches an error
    :param interaction: The slash command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, exceptions.UserBlacklisted):
        """
        The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
        the @checks.is_owner() check in your command, or you can raise the error by yourself.
        
        'hidden=True' will make so that only the user who execute the command can see the message
        """
        embed = disnake.Embed(
            title="Error!",
            description="Você está proibido de utilizar os comandos da Sophia!",
            color=0xE02B2B
        )
        print("Um usuário proibido tentou utilizar a Sophia.")
        return await interaction.send(embed=embed, ephemeral=True)
    elif isinstance(error, commands.errors.MissingPermissions):
        embed = disnake.Embed(
            title="Erro!",
            description="Você não tem permissões `" + ", ".join(
                error.missing_permissions) + "` para executar esse comando!",
            color=0xE02B2B
        )
        print("Um membro proibido tentou usar a Sophia")
        return await interaction.send(embed=embed, ephemeral=True)
    raise error


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {context.guild.name} (ID: {context.message.guild.id}) by {context.message.author} (ID: {context.message.author.id})")


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param context: The normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = disnake.Embed(
            title="Hey, calma lá.",
            description=f"Você pode usar esse comando novamente em {f'{round(hours)} horas' if round(hours) > 0 else ''} {f'{round(minutes)} minutos' if round(minutes) > 0 else ''} {f'{round(seconds)} segundos' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = disnake.Embed(
            title="Erro!",
            description="Você não tem permissão `" + ", ".join(
                error.missing_permissions) + "` para usar esse comando!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = disnake.Embed(
            title="Erro!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error
#### Event ####
@bot.event
async def on_member_join(member):
    print(f"{member} entrou no servidor")
    welcome_channel = bot.get_channel(977015629502627900)
    await welcome_channel.send(f"Bem vindo à minha casa {member.mention}, espero que você goste!", file=disnake.File('images/welcome.png'))

@bot.event
async def on_member_remove(member):
    print(f"{member} saiu do servidor")
    welcome_channel = bot.get_channel(977015629502627900)
    await welcome_channel.send(f"Adeus {member.mention}, até a próxima...", file=disnake.File('images/bye.png'))

bot.run(config["token"])