from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from helpers import checks
import disnake
import random
import requests
class Template(commands.Cog, name="template-slash"):
    def __init__(self, bot):
        self.bot = bot
#Raiva
    @commands.slash_command(
        name="raiva",
        description="Consiga uma fotinha minha com raiva.. Grr",
    )

    @checks.not_blacklisted()

    async def raiva(self, interaction: ApplicationCommandInteraction):
        raivafalas = ['Você me irrita!', 'Seu idiota!', 'Seu otário!', 'Seu babaca!',
                      'Pare de me atormentar', 'Eu vou te bater!', 'Horrendo!', 'Está me deixando nevosa!']
        raivaimg = ['images/angry1.png',
                    'images/angry2.png', 'images/angry3.png']
        await interaction.send(random.choice(raivafalas), file=disnake.File(random.choice(raivaimg)))

#Feliz
    @commands.slash_command(
        name="feliz",
        description="Consiga uma fotinha minha alegre. Yup",
    )

    @checks.not_blacklisted()
    async def feliz(self, interaction: ApplicationCommandInteraction):
        felizfalas = ['A vida é tão bela!', 'Que vontade de cantarrrr.', 'Hoje é dia de Vava ︻┳═一', 'Subi de elo ^^ no vava',
                      'Mãe tá platina xD', 'Yuumi tá open *-*', 'Mais um dia sem ifunny :)', 'Lançou capítulo novo no MangaToon ♥', 'Vamos jogar Lol >.<']
        felizimg = ['images/happy1.png', 'images/happy2.png',
                    'images/happy3.png', 'images/happy4.png']
        await interaction.send(random.choice(felizfalas), file=disnake.File(random.choice(felizimg)))

    @commands.slash_command(
        name="triste",
        description="Quem faz o palhaço rir? :(",
    )
    @checks.not_blacklisted()
    async def triste(self, interaction: ApplicationCommandInteraction):
        tristefalas = ['Perdi no lol :(', 'Acabou meu anime favorito...', 'Contaram para o Jotaro que eu não comi tudo (._.', 'Nisekoi acabou :(', 'Meu rato fugiu',
                       'Sacudi a garrafa do café e estava vazia', 'Meu pc não roda esse jogo', 'Estou longe de você..', 'Não sei matemática básica ;(', 'Baniram Yuumi x-x']
        tristeimg = ['images/sad1.png', 'images/sad2.png',
                     'images/sad3.png', 'images/sad4.png']
        await interaction.send(random.choice(tristefalas), file=disnake.File(random.choice(tristeimg)))

    @commands.slash_command(
        name="anime",
        description="Eu vou escolher um anime pra você!",
    )

    @checks.not_blacklisted()

    async def anime(self, interaction: ApplicationCommandInteraction):
        animeget = requests.get('https://api.jikan.moe/v4/random/anime')
        nameanime = animeget.json()
        name1 = nameanime["data"]["title"]
        await interaction.send("Para você eu recomendo o anime **" + name1 + "**")

    @commands.slash_command(
        name="manga",
        description="Eu vou escolher um mangá pra você!",
    )

    @checks.not_blacklisted()

    async def manga(self, interaction: ApplicationCommandInteraction):
        animeget = requests.get('https://api.jikan.moe/v4/random/manga')
        nameanime = animeget.json()
        name1 = nameanime["data"]["title"]
        await interaction.send("Você tem que ler **" + name1 + "**")

    @commands.slash_command(
        name="presidente",
        description="Sophia lhe dará uma dica para as eleições de 2022",
    )
    @checks.not_blacklisted()
    async def presidente(self, interaction: ApplicationCommandInteraction):      
        await interaction.send("É BOLSONARO OU NÃO É?")



def setup(bot):
    bot.add_cog(Template(bot))
