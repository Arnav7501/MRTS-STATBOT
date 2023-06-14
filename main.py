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

load_dotenv()
APIKEY = os.getenv('APIKEY')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def scrape_wiki(unitName):
    try:
        url = f"https://mrts.fandom.com/wiki/{unitName}"

    # Send a GET request to fetch the HTML content
        response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(response.content, "html.parser")

# Extract the desired information


# Print the extracted information

        td_tag = soup.find("div", class_="mw-parser-output")

# Extract the text content of the td tag
        content = td_tag.text.strip() if td_tag else None

        array = [line for line in content.split("\n") if line.strip()]
        images = soup.find_all('img')
        image = images[1].get('src')
        array.append(image)
        return array

    except Exception as e:
        return 1


async def statScraper(unitName, message):
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

    if message.content.startswith(';rankdps'):
        singleTargetArray = ["Archer", "Swordman",
                             "Knight", "Longbower", "Crossbower", "Ballista"]
        splashArray = ["Mage", "Wizard", "Catapult"]
        singleTargetDictionary = {}
        splashTargetDictionary = {}
        for i in range(len(singleTargetArray)):
            tempValue = scrape_wiki(singleTargetArray[i])
            singleTargetDictionary[tempValue[0]] = tempValue[21]
        sorted_dict = dict(
            sorted(singleTargetDictionary.items(), key=lambda x: x[1]))
        print("SORTED_DICT", sorted_dict)
        embed = Embed()
        embed.title = "Single Target"

        for key in sorted_dict:
            embed.add_field(name=key, value=sorted_dict[key], inline=False)
        await message.channel.send(embed=embed)

        for i in range(len(splashArray)):
            tempValue = scrape_wiki(splashArray[i])
            splashTargetDictionary[tempValue[0]] = tempValue[23]
        sorted_dict = dict(
            sorted(splashTargetDictionary.items(), key=lambda x: x[1]))
        print("SORTED_DICT", sorted_dict)
        embed = Embed()
        embed.title = "Splash Target"
        for key in sorted_dict:
            embed.add_field(name=key, value=sorted_dict[key], inline=False)
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
