import discord
from discord import app_commands
from discord.ext import commands
import random

class RockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rockpaperscissors", description="Play Rock Paper Scissors")
    @app_commands.describe(choice="Your choice: rock, paper, or scissors")
    async def rockpaperscissors(self, interaction: discord.Interaction, choice: str):
        # choice validation and case stuff
        choice = choice.lower()
        if choice not in ["rock", "paper", "scissors"]:
            # make invalid choice embed
            embed = discord.Embed(
                title="Invalid Choice",
                description="You can only choose rock, paper or scissors! Try again",
                color=discord.Color.red()
            )
        else:
            # generate random choice for bot
            botchoice = random.choice(["rock", "paper", "scissors"])
            # determine outcome
            if choice == botchoice:
                outcome = "Its a draw!"
            elif (choice == "rock" and botchoice == "scissors") or (choice == "paper" and botchoice == "rock") or (choice == "scissors" and botchoice == "paper"):
                outcome = "You win!"
            else:
                outcome = "PartyBot wins!"
            # make the outcome embed
            embed = discord.Embed(
                title="Rock Paper Scissors",
                description=f"You chose {choice}\nPartyBot chose...... {botchoice}!!!\n{outcome}",
                color=discord.Color.red()
            )
        embed.set_author(name="PartyBot")
        # send the embed to the channel
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(RockPaperScissors(bot))