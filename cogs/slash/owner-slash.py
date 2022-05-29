""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import json

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

from helpers import json_manager, checks


class Owner(commands.Cog, name="owner-slash"):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(
        name="blacklist",
        description="lista de todos os usuários na blacklist",
    )
    @checks.is_owner()
    async def blacklist(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.
        :param interaction: The application command interaction.
        """
        pass

    @blacklist.sub_command(
        base="blacklist",
        name="add",
        description="Adicione um usuário à blacklist.",
        options=[
            Option(
                name="user",
                description="Usuário que você deseja adicionar na blacklist",
                type=OptionType.user,
                required=True
            )
        ],
    )
    @checks.is_owner()
    async def blacklist_add(self, interaction: ApplicationCommandInteraction, user: disnake.User = None) -> None:
        """
        Lets you add a user from not being able to use the bot.
        :param interaction: The application command interaction.
        :param user: The user that should be added to the blacklist.
        """
        try:
            user_id = user.id
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            if user_id in blacklist['ids']:
                embed = disnake.Embed(
                    title="Erro!",
                    description=f"**{user.name}** já está na blacklist",
                    color=0xE02B2B
                )
                return await interaction.send(embed=embed)
            json_manager.add_user_to_blacklist(user_id)
            embed = disnake.Embed(
                title="Usuário na blacklist",
                description=f"**{user.name}** foi adicionado à blacklist, respeite as regras!",
                color=0x9C84EF
            )
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"Há agora {len(blacklist['ids'])} usuários na blacklist"
            )
            await interaction.send(embed=embed)
        except Exception as exception:
            embed = disnake.Embed(
                title="Erro!",
                description=f"Ocorreu um erro desconhecido ao tentar adicionar **{user.name}** à blacklist.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
            print(exception)

    @blacklist.sub_command(
        base="blacklist",
        name="remove",
        description="Remova um usuário da blacklist.",
        options=[
            Option(
                name="user",
                description="Usuário que você deseja remover da blacklist.",
                type=OptionType.user,
                required=True
            )
        ],
    )
    @checks.is_owner()
    async def blacklist_remove(self, interaction: ApplicationCommandInteraction, user: disnake.User = None):
        """
        Lets you remove a user from not being able to use the bot.
        :param interaction: The application command interaction.
        :param user: The user that should be removed from the blacklist.
        """
        try:
            json_manager.remove_user_from_blacklist(user.id)
            embed = disnake.Embed(
                title="Usuário removido da blacklist",
                description=f"**{user.name}** foi removido da blacklist, aproveite essa segunda chance",
                color=0x9C84EF
            )
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"Há agora {len(blacklist['ids'])} usuários na blacklist"
            )
            await interaction.send(embed=embed)
        except ValueError:
            embed = disnake.Embed(
                title="Erro!",
                description=f"**{user.name}** não está na blacklist.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
        except Exception as exception:
            embed = disnake.Embed(
                title="Erro!",
                description=f"Um erro desconhecido ocorreu a tentar adicionar **{user.name}** à blacklist.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
            print(exception)


def setup(bot):
    bot.add_cog(Owner(bot))
