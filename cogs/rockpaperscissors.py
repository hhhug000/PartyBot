import discord
from discord import app_commands
from discord.ext import commands
import random
import stats

class RockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rockpaperscissors", description="Play Rock Paper Scissors")
    @app_commands.describe(choice="Your choice: rock, paper, or scissors", ranked="Play ranked or no? Default is false")
    async def rockpaperscissors(self, interaction: discord.Interaction, choice: str, ranked: bool = False):
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
                if ranked:
                    outcome = "Its a draw! No points gained or lost"
            elif (choice == "rock" and botchoice == "scissors") or (choice == "paper" and botchoice == "rock") or (choice == "scissors" and botchoice == "paper"):
                outcome = "You win!"
                if ranked:
                    stats.add_score(int(interaction.user.id), 10)
                    outcome = "You win and gain 10 points!"
            else:
                outcome = "PartyBot wins!"
                if ranked:
                    stats.add_score(int(interaction.user.id), -10)
                    outcome = "PartyBot wins and you lose 10 points!"
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