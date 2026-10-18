import discord
from discord import app_commands
from discord.ext import commands
import stats

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # About command, tells users about partybot
    @app_commands.command(name="about", description="About PartyBot")
    async def about(self, interaction: discord.Interaction):
        # create embed to make it look pretty
        embed = discord.Embed(
            title="About PartyBot",
            description="PartyBot lets you play minigames in your discord server!\nTo use PartyBot run one of the minigame commands, to find some run the `/help` command",
            color=discord.Color.red()
        )
        embed.set_author(name="PartyBot")
        # send the embed to the channel
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Help with PartyBot")
    async def help(self, interaction: discord.Interaction):
        # use list of commands so i dont need to change the embed every time
        commands = [
            {
                "command": "/about",
                "description": "Get to know about PartyBot" 
            },
            {
                "command": "/help",
                "description": "This command! Tells you about all the commands"
            },
            {
                "command": "/rockpaperscissors",
                "description": "Play Rock Paper Scissors againt PartyBot"
            },
            {
                "command": "/dice",
                "description": "Roll a dice"
            },
            {
                "command": "/coinflip",
                "description": "Flip a coin"
            }
        ]
        # convert the list into big text
        commandtext = ""
        for command in commands:
            commandtext = commandtext + f"`{command["command"]}`\n{command["description"]}\n\n"
        # again make embed
        embed = discord.Embed(
            title="Help",
            description=f"These are all the commands you can use with partybot, and how to use them:\n\n{commandtext}",
            color=discord.Color.red()
        )
        embed.set_author(name="PartyBot")
        # send it
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="score", description="Check a score")
    @app_commands.describe(user="The user to check the score of (you by default)")
    async def score(self, interaction: discord.Interaction, user: discord.User = None):
        # get the current user if not specified
        if user is None:
            user = interaction.user
        # get the score from the database
        score = stats.get_score(int(user.id))
        # make an embed
        embed = discord.Embed(
            title=f"{user.name}'s Score",
            description=f"{user.name} has {score} points",
            color=discord.Color.red()
        )
        embed.set_author(name="PartyBot")
        # send the embed
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leaderboard", description="Check the leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        # defer stops it from timing out, so instead of send_message use followup
        await interaction.response.defer()
        # Get leaderboard from db
        leaderboard = stats.get_leaderboard()
        leaderboardtext = ""
        for i, (user_id, score) in enumerate(leaderboard):
            try:
                # fetch the user
                user = await self.bot.fetch_user(user_id)
                username = user.name
            except (discord.NotFound, discord.HTTPException):
                # this is for when user accounts are deleted
                username = f"Unknown User ({user_id})"
            leaderboardtext += f"{i+1}. {username}: {score} points\n"
        if not leaderboardtext:
            leaderboardtext = "No scores recorded yet!"

        # make embed
        embed = discord.Embed(
            title="Leaderboard",
            description=f"The top 5 users are\n{leaderboardtext}",
            color=discord.Color.red()
        )
        embed.set_author(name="PartyBot")
        
        # send the embed
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))