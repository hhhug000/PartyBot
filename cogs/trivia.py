import discord
from discord import app_commands
from discord.ext import commands
import stats
import random
import asyncio

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="trivia", description="Play some trivia")
    @app_commands.describe(category="The category of trivia to play (default is random)")
    async def trivia(self, interaction: discord.Interaction, category: str = "random"):
        # get trivia questions
        categories = stats.get_trivia_categories()
        if category.lower() != "random" and category.lower() not in categories:
            embed = discord.Embed(
                title="Invalid Category",
                description=f"Invalid category! Please choose from the following\n{', '.join(categories)}",
                color=discord.Color.red()
            )
            embed.set_author(name="PartyBot")

            await interaction.response.send_message(embed=embed)
            return
        else:
            if category.lower() == "random":
                category = random.choice(categories)
            try:
                question, answer, choices = stats.get_trivia_questions(category.lower())
            except (OSError, ValueError):
                await interaction.response.send_message(
                    "I couldn't load a trivia question right now. Please try again."
                )
                return
            correct_index = choices.index(answer)
            emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
            choice_lines = "\n".join(
                f"{emojis[index]} {choice}"
                for index, choice in enumerate(choices)
            )

            # make the embed
            embed = discord.Embed(
                title="Trivia",
                description=(
                    f"Your category is {category}\n\n"
                    f"{question}\n\n"
                    f"Choices:\n{choice_lines}"
                ),
                color=discord.Color.red()
            )
            embed.set_author(name="PartyBot")

            await interaction.response.send_message(embed=embed)
            message = await interaction.original_response()

            for emoji in emojis[:len(choices)]:
                await message.add_reaction(emoji)

            def check(reaction, user):
                return (
                    reaction.message.id == message.id
                    and not user.bot
                    and str(reaction.emoji) in emojis[:len(choices)]
                )

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await interaction.followup.send(f"Nobody answered in time, the correct answer was **{answer}**")
                return

            chosen_emoji = str(reaction.emoji)
            chosen_index = emojis.index(chosen_emoji)

            if chosen_index == correct_index:
                response_embed = discord.Embed(
                    title="Correct!",
                    description=f"{user.mention} got it right! The answer was {choices[correct_index]}",
                    color=discord.Color.green()
                )
            else:
                response_embed = discord.Embed(
                    title="Incorrect",
                    description=f"{user.mention} guessed {choices[chosen_index]}, the correct answer was {choices[correct_index]}",
                    color=discord.Color.red()
                )
            response_embed.set_author(name="PartyBot")

            await message.edit(embed=response_embed)


    

async def setup(bot):
    await bot.add_cog(Trivia(bot))