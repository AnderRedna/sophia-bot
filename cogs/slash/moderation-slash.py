""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

from helpers import checks


class Moderation(commands.Cog, name="moderation-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="kick",
        description="Chute um usuário para fora do servidor.",
        options=[
            Option(
                name="user",
                description="Usuário que você deseja chutar.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="Razão",
                type=OptionType.string,
                required=False
            )
        ]
    )
    @commands.has_permissions(kick_members=True)
    @checks.not_blacklisted()
    async def kick(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                   reason: str = "Not specified") -> None:
        """
        Kick a user out of the server.
        :param interaction: The application command interaction.
        :param user: The user that should be kicked from the server.
        :param reason: The reason for the kick. Default is "Not specified".
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = disnake.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
        else:
            try:
                embed = disnake.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await interaction.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{interaction.author}**!\nReason: {reason}"
                    )
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.kick(reason=reason)
            except:
                embed = disnake.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B
                )
                await interaction.send(embed=embed)

    @commands.slash_command(
        name="ban",
        description="Banir um usuário do servidor.",
        options=[
            Option(
                name="user",
                description="Usuário que você deseja banir",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="razão",
                description="Razão do banimento do usuário",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    async def ban(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                  reason: str = "Não especificada") -> None:
        """
        Bans a user from the server.
        :param interaction: The application command interaction.
        :param user: The user that should be banned from the server.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        try:
            if member.guild_permissions.administrator:
                embed = disnake.Embed(
                    title="Erro!",
                    description="Usuário possui permissões de administrador",
                    color=0xE02B2B
                )
                await interaction.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Usuário BANIDO!",
                    description=f"**{member}** foi banido por **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Razão:",
                    value=reason
                )
                await interaction.send(embed=embed)
                try:
                    await member.send(f"Você foi banido por **{interaction.author}**!\nRazão: {reason}")
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=reason)
        except:
            embed = disnake.Embed(
                title="Erro!",
                description="Erro ao banir o usuário, certifique se o usuário possui um cargo maior que o seu",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)

    @commands.slash_command(
        name="warn",
        description="Envie um aviso para algum usuário do servidor.",
        options=[
            Option(
                name="user",
                description="Usuário que você deseja enviar o aviso.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="Motivo do aviso.",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def warn(self, interaction: ApplicationCommandInteraction, user: disnake.User,        
                   reason: str = "Not specified") -> None:

        """
        Warns a user in his private messages.
        :param interaction: The application command interaction.
        :param user: The user that should be warned.
        :param reason: The reason for the warn. Default is "Not specified".
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        embed = disnake.Embed(
            title="User Warned!",
            description=f"**{member}** foi avisado por **{interaction.author}**!",
            color=0x9C84EF
        )
        embed.add_field(
            name="Razão:",
            value=reason
        )          
        await interaction.send(embed=embed)
        try:       
            await member.send(f"Você recebeu um aviso de **{interaction.author}**!\nRazão: {reason}", file=disnake.File('images/warn1.png'))            
        except disnake.Forbidden:
            # Couldn't send a message in the private messages of the user           
            await interaction.send(f"{member.mention}, você recebeu um aviso de **{interaction.author}**!\nRazão: {reason}", file=disnake.File('images/warn1.png'))       
               
    @commands.slash_command(
        name="purge",
        description="Delete um número determinado de mensagens",
        options=[
            Option(
                name="amount",
                description="Quantidade de mensagens que você deseja deletar. (Entre 1 a 100.)",
                type=OptionType.integer,
                required=True,
                min_value=1,
                max_value=100
            )
        ],
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def purge(self, interaction: ApplicationCommandInteraction, amount: int) -> None:
        """
        Delete a number of messages.

        :param interaction: The application command interaction.
        :param amount: The number of messages that should be deleted.
        """
        purged_messages = await interaction.channel.purge(limit=amount)
        embed = disnake.Embed(
            title="Chat limpo!",
            description=f"**{interaction.author}** mensagens removidas:  **{len(purged_messages)}**",
            color=0x9C84EF
        )
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="hackban",
        description="Banir um usuário sem que o mesmo esteja no servidor.",
        options=[
            Option(
                name="user_id",
                description="ID do usuário que você deseja banir.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="reason",
                description="Razão do banimento.",
                type=OptionType.string,
                required=False
            )
        ]
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    async def hackban(self, interaction: ApplicationCommandInteraction, user_id: str,
                      reason: str = "Not specified") -> None:
        """
        Bans a user without the user having to be in the server.
        :param interaction: The application command interaction.
        :param user_id: The ID of the user that should be banned.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        try:
            await self.bot.http.ban(user_id, interaction.guild.id, reason=reason)
            user = await self.bot.get_or_fetch_user(int(user_id))
            embed = disnake.Embed(
                title="User Banned!",
                description=f"**{user} (ID: {user_id}) ** was banned by **{interaction.author}**!",
                color=0x9C84EF
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            await interaction.send(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
            print(e)


def setup(bot):
    bot.add_cog(Moderation(bot))
