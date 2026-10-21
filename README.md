# PartyBot
The party game bot for discord

## Commands

### General

- `/about`: Sends an about message
- `/help`: Lists all the commands in PartyBot

### Games

- `/rockpaperscissors`: Lets the user play rock paper scissors against PartyBot, takes in a choice and if the user wants to play ranked or not
- `/dice`: Lets the user roll any dice, takes in a string like 2d16 or 5d8, the default is 1d6
- `/coinflip`: Flips a coin for the user
- `/trivia`: Asks the user trivia questions, first person to reply wins, takes in a category, and if the user wants to play ranked or not, it takes an answer with message reactions

### Scoring

- `/score`: Finds a users score, by default the user who sent the command
- `/leaderboard`: Shows the top 5 users globally across all servers on this PartyBot instance

## Scoring

Some PartyBot games have the option to play ranked, If a user chooses to play ranked they will gain or lose points based on game outcomes.

Scores are stored in a SQLite database.

## Want to try?

If you want to try PartyBot, there is a demo instance running on this discord server:
[https://discord.gg/2HpgPBjUxq](https://discord.gg/2HpgPBjUxq)

## Trivia Dataset
The trivia dataset is taken from itmmckernan/triviaJSON on github