""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import random

import aiohttp
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from helpers import checks


class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    @disnake.ui.button(label="Cara", style=disnake.ButtonStyle.blurple)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="Coroa", style=disnake.ButtonStyle.blurple)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()


class RockPaperScissors(disnake.ui.Select):
    def __init__(self):

        options = [
            disnake.SelectOption(
                label="Tesoura", description="Você escolheu tesoura.", emoji="✂"
            ),
            disnake.SelectOption(
                label="Pedra", description="Você escolheu pedra.", emoji="🪨"   
            ),
            disnake.SelectOption(
                label="Papel", description="Você escolheu papel.", emoji="🧻"
            ),
        ]

        super().__init__(
            placeholder="Escolha...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        choices = {
            "pedra": 0,
            "papel": 1,
            "tesoura": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = disnake.Embed(color=0x9C84EF)
        result_embed.set_author(name=interaction.author.display_name, icon_url=interaction.author.avatar.url)

        if user_choice_index == bot_choice_index:
            result_embed.description = f"**Foi um empate HAHA!**\nVocê escolheu {user_choice} e eu escolhi {bot_choice}."
            result_embed.colour = 0xF59E42
        elif user_choice_index == 0 and bot_choice_index == 2:
            result_embed.description = f"**Eu... Perdi!**\nVocê escolheu {user_choice} e eu escolhi {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 1 and bot_choice_index == 0:
            result_embed.description = f"**Foi uma batalha lendária!**\nVocê escolheu {user_choice} e eu escolhi {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 2 and bot_choice_index == 1:
            result_embed.description = f"**Não é possível**\nVocê escolheu {user_choice} e eu escolhi: {bot_choice}."
            result_embed.colour = 0x9C84EF
        else:
            result_embed.description = f"**EU VENCI NYA!**\nVocê escolheu {user_choice} e eu escolhi {bot_choice} nya!."
            result_embed.colour = 0xE02B2B
        await interaction.response.defer()
        await interaction.edit_original_message(embed=result_embed, content=None, view=None)


class RockPaperScissorsView(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="moeda",
        description="Vamos jogar a moeda, lembre-se, isso é sagrado!!."
    )
    @checks.not_blacklisted()
    async def moeda(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Make a coin flip, but give your bet before.
        :param interaction: The application command interaction.
        """
        buttons = Choice()
        embed = disnake.Embed(
            description="Qual sua aposta?",
            color=0x9C84EF
        )
        await interaction.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["Coroa", "Cara"])
        if buttons.choice == result:
            # User guessed correctly
            embed = disnake.Embed(
                description=f"Você escolheu `{buttons.choice}`.  a moeda caiu em `{result}`... Na próxima vez eu ganho!!!.",
                color=0x9C84EF
            )
        else:
            embed = disnake.Embed(
                description=f"Você escolheu `{buttons.choice}`.  a moeda caiu em `{result}`. Eu ganhei hihi.",
                color=0xE02B2B
            )
        await interaction.edit_original_message(embed=embed, view=None)

    @commands.slash_command(
        name="ppt",
        description="Shophia irá jogar pedra papel e tesoura com você."
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Play the rock paper scissors game against the bot.
        :param interaction: The application command interaction.
        """
        view = RockPaperScissorsView()
        await interaction.send("Por favor, faça a sua escolha", view=view)


def setup(bot):
    bot.add_cog(Fun(bot))
