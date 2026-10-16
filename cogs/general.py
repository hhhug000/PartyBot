import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # About command, tells users about partybot
    @app_commands.command(name="about", description="About PartyBot")
    async def ping(self, interaction: discord.Interaction):
        # create embed to make it look pretty
        embed = discord.Embed(
            title="About PartyBot",
            description="PartyBot lets you play minigames in your discord server!\nTo use PartyBot run one of the minigame commands, to find some run the `/help` command",
            color=discord.Color.red()
        )
        embed.set_author(name="PartyBot")
        # send the embed to the channel
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))