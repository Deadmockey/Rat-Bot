"""
This is a discord bot that is used for dumb stuff I think is funny
"""

import os, time, validators
import discord, discord.ui
from urllib.parse import urlparse, urlunparse
from dotenv import load_dotenv

load_dotenv()

#test

class TimezoneDateModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Enter a date")

    tz_date = discord.ui.InputText(
        style=discord.InputTextStyle.short,
        label="date",
        required=True,
        placeholder="Enter in a date",
    )


def run():
    # Creating the bot
    TOKEN = os.getenv("RATBOTTOKEN")
    rat_bot = discord.Bot(intents=discord.Intents.all())

    # Words used in kms and kys detection
    kms_words = ["kms", "kill my self"]
    kys_word = ["kys", "kill your self"]

    @rat_bot.event
    async def on_connect():
        if rat_bot.auto_sync_commands:
            await rat_bot.sync_commands()
        print(f"{rat_bot.user} connected")

    @rat_bot.event
    async def on_ready():
        """
        This runs when the bot is started
        Prints a statement when online
        """
        print(f"{rat_bot.user} is ready and online")

    @rat_bot.slash_command(name="hello", description="Say hello to the bot")
    async def hello(ctx: discord.ApplicationContext):
        """
        Simple Hello Command
        """
        await ctx.respond("Hey!")

    @rat_bot.listen()
    async def on_message(message: discord.Message):
        """
        Detects when a twitter link is posted and
        changes it to fxtwitter
        """
        if (
            validators.url(message.content) is True
            and message.author != rat_bot.user
            and ("//twitter.com" in message.content or "//x.com" in message.content)
        ):
            channel = message.channel

            parsed_url = urlparse(message.content)
            desired_url = urlunparse(parsed_url._replace(netloc="vxtwitter.com"))
            await message.delete()

            await channel.send(
                f"{(message.author.display_name).title()} posted {desired_url}"
            )

    @rat_bot.listen("on_message")
    async def message(message: discord.Message):
        """
        Detects when user says some form of 'kill my self" and
        replies with an image
        """
        if (
            any(word in message.content for word in kms_words)
            and message.author != rat_bot.user
        ):
            await message.reply(
                "https://cdn.discordapp.com/attachments/796868040096350244/1255343773903360030/jpeg_1719257480000.jpg?ex=667cc97e&is=667b77fe&hm=c7616b688b14bd5dc286215b8706552b2ae8c2c8a247f19a852a0770094fc99b&"
            )

    @rat_bot.slash_command(name="psychic", description="Let the bot read your mind")
    async def psychic(ctx: discord.ApplicationContext):
        """
        Stupid game where you input a number and the bot will "guess"
        what number you are thinking of
        """
        await ctx.respond(
            "Think of a number and write it down. I will then read your mind"
        )
        guess: discord.Message = await rat_bot.wait_for(
            "message", check=lambda message: message.author == ctx.author
        )

        loading = await ctx.send_followup("reading your mind.")
        for i in range(int(len(guess.content) / 10) + 1):
            time.sleep(0.5)
            await loading.edit(content="reading your mind..")
            time.sleep(0.5)
            await loading.edit(content="reading your mind...")
            time.sleep(0.5)
            await loading.edit(content="reading your mind.")
            if i == 6:
                break
        time.sleep(0.5)
        await loading.edit(content="reading your mind..")

        if (guess.content).isnumeric():
            await loading.edit(
                content=f"You were thinking of the number **{guess.content}**"
            )
        elif len(guess.content) < 50:
            await loading.edit(
                content=f"Nice try, but you were thinking of **{guess.content}**"
            )
        else:
            await loading.edit(
                content=f"Sorry I can't read your mind. You are thinking too much"
            )

    rat_bot.run(TOKEN)

    @rat_bot.slash_command(
        name="autotimezone",
        description="Change your date to match other peoples timezones",
    )
    async def autotimezone(ctx: discord.ApplicationContext):
        timezone_date_modal = TimezoneDateModal()
        await ctx.send_modal(timezone_date_modal)


run()
