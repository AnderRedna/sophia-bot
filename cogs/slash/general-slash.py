""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import platform
import random
from turtle import heading

import aiohttp
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from fastapi import File
import requests

from helpers import checks


class General(commands.Cog, name="general-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="botinfo",
        description="Consiga algumas informações sobre mim!",
    )
    @checks.not_blacklisted()
    async def botinfo(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Get some useful (or not) information about the bot.
        :param interaction: The application command interaction.
        """
        embed = disnake.Embed(
            description="Pra namorar comigo tem que ganhar x1 do meu pai!",
            color=0x9C84EF
        )
        embed.set_author(
            name="Sophia-chan"
        )
        embed.add_field(
            name="Nome:",
            value="Sophia Tsukimi",
            inline=True
        )
        embed.add_field(
            name="Idade:",
            value="16",
            inline=True
        )
        embed.add_field(
            name="Gênero:",
            value="Waifu",
            inline=True
        )
        embed.add_field(
            name="Gênero favorito:",
            value="Romance",
            inline=True
        )
        embed.add_field(
            name="Cor favorita:",
            value="Branco",
            inline=True
        )
        embed.add_field(
            name="Animal favorito:",
            value="Rato",
            inline=True
        )
        embed.add_field(
            name="Anime favorito:",
            value="Toradora",
            inline=True
        )
        embed.add_field(
            name="Mangá favorito:",
            value="Nisekoi",
            inline=True
        )
        embed.add_field(
            name="Jogo favorito:",
            value="Gartic",
            inline=True
        )
        
        embed.add_field(
            name="Prefixo:",
            value=f"/ (Comandos Slash) ou {self.bot.config['prefix']} para comandos normais!",
            inline=False
        )
        embed.set_footer(
            text="_Uma fã secreta do Ifunny_"
        )
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Get some useful (or not) information about the server.
        :param interaction: The application command interaction.
        """
        roles = [role.name for role in interaction.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = disnake.Embed(
            title="**Nome do servidor:**",
            description=f"{interaction.guild}",
            color=0x9C84EF
        )
        embed.set_thumbnail(
            url=interaction.guild.icon.url
        )
        embed.add_field(
            name="Membros",
            value=interaction.guild.member_count
        )
        embed.add_field(
            name="Canais de Texto/Voz",
            value=f"{len(interaction.guild.channels)}"
        )
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="site",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def site(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Get some useful (or not) information about the server.
        :param interaction: The application command interaction.
        """
        roles = [role.name for role in interaction.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = disnake.Embed(
            title="**Site: **",
            description=f"http://MangaToon.com.br",
            color=0x9C84EF
        )
        embed.set_thumbnail(
            url='https://img.anime2you.de/2022/05/Marin-Kitagawa.jpg'          
        )
       
        await interaction.send(embed=embed)




    @commands.slash_command(
        name="ping",
        description="Verificar se estou viva.",
    )
    @checks.not_blacklisted()
    async def ping(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Check if the bot is alive.
        :param interaction: The application command interaction.
        """
        embed = disnake.Embed(
            title="🏓 Pong!",
            description=f"A latência é {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="convidar",
        description="Me coloque no seu servidor!",
    )
    @checks.not_blacklisted()
    async def convidar(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Get the invite link of the bot to be able to invite it.
        :param interaction: The application command interaction.
        """
        embed = disnake.Embed(
            description=f"Minha casa é o MangáToon, meu pai brigaria comigo se soubesse que eu traí o movimento!\n Lamento mas você não pode me convidar.",
            color=0xD75BF4
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await interaction.author.send(embed=embed)
            await interaction.send("Te mandei uma menssagem no pv!")
        except disnake.Forbidden:
            await interaction.send(embed=embed)

    @commands.slash_command(
        name="pergunta",
        description="Faça uma pergunta à Sophia.",
        options=[
            Option(
                name="pergunta",
                description="Escreva a sua pergunta. ",
                type=OptionType.string,
                required=True
            )
        ],
    )
    @checks.not_blacklisted()
    async def eight_ball(self, interaction: ApplicationCommandInteraction, question: str) -> None:
        """
        Ask any question to the bot.
        :param interaction: The application command interaction.
        :param question: The question that should be asked by the user.
        """
        answers = ["It is certain.", "It is decidedly so.", "You may rely on it.", "Without a doubt.",
                   "Yes - definitely.", "As I see, yes.", "Most likely.", "Outlook good.", "Yes.",
                   "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                   "Cannot predict now.", "Concentrate and ask again later.", "Don't count on it.", "My reply is no.",
                   "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = disnake.Embed(
            title="**Minha resposta:**",
            description=f"{random.choice(answers)}",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"A pergunta foi: {question}"
        )
        await interaction.send(embed=embed) 
def setup(bot):
    bot.add_cog(General(bot))
