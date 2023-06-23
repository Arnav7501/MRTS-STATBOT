# This example requires the 'message_content' intent.
from discord.ext import tasks, commands
import discord
from discord import Embed
import patchnotes
import re
import os
from dotenv import load_dotenv
import datetime
from rank import rankingList, splashRankingList
from elo import eloSystem, calculateEloRating, getUserInfo
from wikiscraper import scrape_wiki
from reactionmenu import ReactionMenu, ReactionButton

load_dotenv()
APIKEY = os.getenv('APIKEY')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix=';', intents=intents)


async def statScraper(unitName, message):
    unitName = unitName.title()
    unitDict = patchnotes.TableToDict(
        "https://pastebin.com/raw/xchHf3Gp")[unitName]
    embed = Embed()
    embed.title = unitName
    for key in unitDict:
        embed.add_field(name=key, value=unitDict[key])
    try:
        embed.add_field(name="Damage per second", value=round(float(
            unitDict["Damage"]/unitDict["Rate"]), 2))
    except:
        pass
    await message.channel.send(embed=embed)


@bot.event
async def on_ready():

    print(f'We have logged in as {bot.user}')
    check_patchnotes.start()


@bot.command()
async def leaderboard(ctx):
    embed = Embed()
    menu = ReactionMenu(ctx, menu_type=ReactionMenu.TypeEmbed)
    embed.title = "Leaderboard"
    table = getUserInfo("all")
    array = {}
    for row in table:
        user = await bot.fetch_user(row[0])
        username = user.name
        array[username] = row[1]
        print(username, row[1])
        sorted_dict = dict(
            sorted(array.items(), key=lambda x: x[1], reverse=True))
    counter = 1
    for key in sorted_dict:
        if counter % 5 != 0:
            embed.add_field(name=key, value=sorted_dict[key], inline=False)
        else:
            embed.add_field(name=key, value=sorted_dict[key], inline=False)
            menu.add_page(embed)
            embed = Embed()
            print(menu)
        counter += 1

    if counter % 5 != 0:
        menu.add_page(embed)

    menu.add_button(ReactionButton.back())
    menu.add_button(ReactionButton.next())
    menu.add_button(ReactionButton.end_session())

    await menu.start(send_to=ctx.channel)


old = patchnotes.TableToDict(
    "https://pastebin.com/raw/xchHf3Gp")


@tasks.loop(minutes=1)  # Set the interval to 1 hour
async def check_patchnotes():
    global old
    variable = patchnotes.PrintChanges(
        old, patchnotes.TableToDict("https://pastebin.com/raw/xchHf3Gp"))
    if (len(variable) > 0):
        channel = bot.get_channel(1109558632292556903)
        await channel.send(variable)
        old = patchnotes.TableToDict("https://pastebin.com/raw/xchHf3Gp")
        await channel.send("DMNKS has changed some stats <@763582841866682368> <@246824672367345674> <@621516858205405197>")

cooldowns = {}


@bot.event
async def on_message(message):
    current_time = datetime.datetime.now()

    if message.author.id in cooldowns and message.content.startswith(';'):
        time_difference = current_time - cooldowns[message.author.id]
        if time_difference.total_seconds() < 10:
            await message.channel.send("You're on cooldown")
            return
        content = message.content[7:]

    if message.content.startswith(';troop'):
        await statScraper(content, message)
    if message.content.startswith(';elo'):
        if message.channel.id == 1120485682369007757:
            content = message.content[4:]
            two_users = []
            both_userids = []
            # getting elos of both players, if the player doesn't exist we give them a default elo of 100
            if message.mentions:
                for user in message.mentions:
                    user_id = user.id
                    both_userids.append(user_id)
                    if getUserInfo(str(user_id)) == False:
                        eloSystem(str(user_id), 100)
                        two_users.append(100)
                    else:
                        two_users.append(getUserInfo(str(user_id)))

            if message.content.split(" ")[3] == "win":
                eloCounterPlayerOne = 1
                eloCounterPlayerTwo = 0
            else:
                eloCounterPlayerOne = 0
                eloCounterPlayerTwo = 1

            valuePlayerOne = calculateEloRating(
                two_users[0], two_users[1], eloCounterPlayerOne)

            valuePlayerTwo = calculateEloRating(
                two_users[1], two_users[0], eloCounterPlayerTwo)

            eloSystem(str(both_userids[0]), valuePlayerOne)
            eloSystem(str(both_userids[1]), valuePlayerTwo)

            await message.channel.send(f"<@{both_userids[0]}> your new elo is {valuePlayerOne}, other player's elo is {valuePlayerTwo}")
        else:
            await message.channel.send("Wrong channel, try matchmaking")
    if message.content.startswith(";help"):
        embed = Embed()
        embed.title = "Help"
        embed.add_field(
            name=";troop", value="Displays the stats of a troop, eg ;troop wizard", inline=False)
        embed.add_field(
            name=";elo @player1 @player2 match_result", value="Calculates the elo of a player. If i beat a player named Shrimp, command would be ;elo @arnav @shrimp win. Note that any false uses of this command will result in instant termination to your access to the bot and possible further consequences. Report any false runs to @arnav1977 so he can revoke the abuser's access. ", inline=False)
        embed.add_field(name=";rank type",
                        value="Displays the top troops by the selected value (dps, health, speed). Note that splash target DPS cannot be compared to single target due to their area of effect.", inline=False)
        embed.add_field(name=";leaderboard",
                        value="Displays the leaderboard of the top players by elo.", inline=False)
        await message.channel.send(embed=embed)
    if message.content.startswith(';rank'):
        param = message.content[6:]
        embed = rankingList(param)
        embed2 = splashRankingList(param)
        await message.channel.send(embed=embed)
        await message.channel.send(embed=embed2)

    if message.content.startswith(';patchnotes'):
        if len(message.content) == 11:
            await message.channel.send(patchnotes.PrintChanges(patchnotes.TableToDict(old), patchnotes.TableToDict("https://pastebin.com/raw/xchHf3Gp")))
        else:
            content = message.content[12:]
            pattern = r'^https?://(?:www\.)?pastebin\.com/raw/[a-zA-Z0-9]+$'
            if (re.match(pattern, content) is None):
                await message.channel.send("i get the feeling that's not a patebin link")
            else:
                await message.channel.send(patchnotes.PrintChanges(patchnotes.TableToDict(content), patchnotes.TableToDict("https://pastebin.com/raw/xchHf3Gp")))
        if message.author.id == 263351384466784257:
            await message.channel.send("you know what would be cool? if you did this already for us")

    cooldowns[message.author.id] = current_time

    await bot.process_commands(message)
bot.run(
    APIKEY)
