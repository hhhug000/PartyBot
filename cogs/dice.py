import discord
from discord import app_commands
from discord.ext import commands
import random

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Dice command, rolls a dice
    @app_commands.command(name="dice", description="Roll a dice")
    @app_commands.describe(dice="The type of dice to roll (1d6 is default)")
    async def dice(self, interaction: discord.Interaction, dice: str = "1d6"):
        rolls = []
        sum = 0
        dicetype = dice.split("d")
        for i in range(int(dicetype[0])):
            roll = random.randint(1, int(dicetype[1]))
            rolls.append(str(roll))
            sum += roll
        # create embed to make it look pretty
        embed = discord.Embed(
            title="Roll the dice",
            description=f"You chose to roll a {dice}\nYour rolls are {" ".join(rolls)},\nIn total you rolled {sum} ",
            color=discord.Color.red()
        )
        embed.set_author(name="PartyBot")
        # send the embed to the channel
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction):
        flip = random.choice(["Heads", "Tails"])
        # pretty embed
        embed = discord.Embed(
            title="Coin Flip",
            description=f"You flipped a coin and got {flip}",
            color=discord.Color.red()
        )
        embed.set_author(name="PartyBot")
        # send it
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Dice(bot))