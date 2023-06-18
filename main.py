# This example requires the 'message_content' intent.
from discord.ext import tasks
import discord
from discord import Embed
import requests
from bs4 import BeautifulSoup
import patchnotes
import re
import os
from dotenv import load_dotenv

from rank import rankingList
from elo import eloSystem, calculateEloRating, getUserInfo
from wikiscraper import scrape_wiki
load_dotenv()
APIKEY = os.getenv('APIKEY')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def statScraper(unitName, message):
    array = []
    array = scrape_wiki(unitName)
    image = array[-1]
    embed = Embed()
    embed.title = array[0]
    if array[13] == 'S-Range':
        embed.add_field(name=array[2], value=array[5])
        embed.add_field(name=array[3], value=array[6])
        embed.add_field(name=array[4], value=array[7])
        embed.add_field(name=array[8], value=array[10])
        embed.add_field(name=array[9], value=array[11])
        embed.add_field(name=array[12], value=array[15])
        embed.add_field(name=array[13], value=array[16])
        embed.add_field(name=array[14], value=array[17])
        embed.add_field(name=array[18], value=array[20])
        embed.add_field(name=array[19], value=array[21])
        embed.add_field(name=array[22], value=array[23])

    else:
        embed.add_field(name=array[2], value=array[5])
        embed.add_field(name=array[3], value=array[6])
        embed.add_field(name=array[4], value=array[7])
        embed.add_field(name=array[8], value=array[10])
        embed.add_field(name=array[9], value=array[11])
        embed.add_field(name=array[12], value=array[14])
        embed.add_field(name=array[13], value=array[15])
        embed.add_field(name=array[16], value=array[18])
        embed.add_field(name=array[17], value=array[19])
        embed.add_field(name=array[20], value=array[21])

    embed.set_image(url=image)
    await message.channel.send(embed=embed)

   # await message.channel.send(f"ERROR, {e}")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    check_patchnotes.start()
    # eloSystem("test", 1000)

old = "https://pastebin.com/raw/xchHf3Gp"
old = patchnotes.TableToDict(old)


@tasks.loop(hours=1)  # Set the interval to 1 hour
async def check_patchnotes():
    global old
    variable = patchnotes.PrintChanges(
        old, patchnotes.TableToDict("https://pastebin.com/raw/xchHf3Gp"))
    if len(variable) > 0:
        channel = client.get_channel(1109558632292556903)
        await channel.send(variable)
        old = patchnotes.TableToDict("https://pastebin.com/raw/xchHf3Gp")
        await channel.send("DMNKS has changed some stats <@763582841866682368> <@246824672367345674> <@621516858205405197>")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(';troop'):
        content = message.content[6:]
        await statScraper(content, message)
    
    if message.content.startswith(';setchannel'):
        content = message.content[12:]
        await message.channel.send(setChannel(content))

    if message.content.startswith(';elo'):
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
                    print(getUserInfo(str(user_id)))
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
        eloSystem(str(both_userids[0]), valuePlayerTwo)

        valuePlayerTwo = calculateEloRating(
            two_users[1], two_users[0], eloCounterPlayerTwo)
        await message.channel.send(f"<@{both_userids[0]}> your new elo is {valuePlayerOne}, other player's elo is {valuePlayerTwo}")
    if message.content.startswith(";help"):
        embed = Embed()
        embed.title = "Help"
        embed.add_field(
            name=";troop", value="Displays the stats of a troop", inline=False)
        embed.add_field(
            name=";elo", value="Calculates the elo of a player", inline=False)
        embed.add_field(name=";rankdps",
                        value="Displays the top single target troops by dps", inline=False)
        embed.add_field(name=";leaderboard",
                        value="Displays the leaderboard", inline=False)
        await message.channel.send(embed=embed)
    if message.content.startswith(';rankdps'):
        embed = rankingList()
        await message.channel.send(embed=embed)

    if message.content.startswith(';leaderboard'):
        embed = Embed()
        embed.title = "Leaderboard"
        table = getUserInfo("all")
        for row in table:
            user = await client.fetch_user(row[0])
            username = user.name
            embed.add_field(name=username, value=row[1], inline=False)
        await message.channel.send(embed=embed)

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
            await message.channel.send("you know what would be cool? if you did this alread for us")


client.run(
    APIKEY)
