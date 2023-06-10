# This example requires the 'message_content' intent.
import discord
import requests
import io
import aiohttp
from bs4 import BeautifulSoup
import patchnotes 
import re
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

old = "https://pastebin.com/raw/neCtnQfG"


async def statScraper(unitName, message):
    try:
        url = f"https://mrts.fandom.com/wiki/{unitName}"

    # Send a GET request to fetch the HTML content
        response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(response.content, "html.parser")

# Extract the desired information


# Print the extracted information
        meta_tag = soup.find("meta", property="og:title")

# Extract the content attribute of the meta tag
        title = meta_tag["content"] if meta_tag else None

        td_tag = soup.find("div", class_="mw-parser-output")

# Extract the text content of the td tag
        content = td_tag.text.strip() if td_tag else None

        array = [line for line in content.split("\n") if line.strip()]
        images = soup.find_all('img')
        image = images[1].get('src')
        print("image is", image)
        if array[13] == 'S-Range':
            await message.channel.send(f"{array[0]}\n-{array[1]}\n{array[2]}: {array[5]}\n{array[3]}: {array[6]}\n{array[4]}: {array[7]}\n{array[8]}: {array[10]}\n{array[9]}: {array[11]}"
                                       f"\n{array[12]}: {array[15]}\n{array[13]}: {array[16]}\n{array[14]}: {array[17]}\n{array[18]}: {array[20]}\n{array[19]}: {array[21]}\n{array[22]}: {array[23]}")
        else:
            await message.channel.send(f"{array[0]}\n-{array[1]}\n{array[2]}: {array[5]}\n{array[3]}: {array[6]}\n{array[4]}: {array[7]}\n{array[8]}: {array[10]}\n{array[9]}: {array[11]}"
                                       f"\n{array[12]}: {array[14]}\n{array[13]}: {array[15]}\n{array[16]}: {array[18]}\n{array[17]}: {array[19]}\n{array[20]}: {array[21]}")

        async with aiohttp.ClientSession() as session:
            async with session.get(image) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                    await message.channel.send(file=discord.File(io.BytesIO(image_bytes), 'image.png'))
                else:
                    await message.channel.send("Failed to fetch the image.")
    except Exception as e:
       # await message.channel.send(f"ERROR, {e}")
        await message.channel.send("Something went wrong. You may be entering the wrong name, or attempting to get information on a special unit, which is not supported yet.")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(';troop'):
        if message.author.id == 450840257282441257:
            await message.channel.send('im eating shrimp right now')
        else:
            content = message.content[6:]
            await statScraper(content, message)
    if message.content.startswith(';patchnotes'):
        if len(message) == 11:
            await message.channel.send(patchnotes.PrintChanges(patchnotes.TableToDict(old), patchnotes.TableToDict("https://pastebin.com/raw/xchHf3Gp")))
        else:
            content = message.content[12:]
            pattern = r'^https?://(?:www\.)?pastebin\.com/raw/[a-zA-Z0-9]+$'
            if(re.match(pattern, content) is None):
                await message.channel.send("i get the feeling that's not a patebin link")
            else:
                await message.channel.send(patchnotes.PrintChanges(patchnotes.TableToDict(content), patchnotes.TableToDict("https://pastebin.com/raw/xchHf3Gp")))
        if message.author.id == 263351384466784257:
            await message.channel.send ("https://media.discordapp.net/attachments/728744216603131925/1115173479097041048/attachment.gif")
    if message.content.startswith(';2elz'):
        await message.channel.send("1. Lack of transparency between administration and the community\n2. Punishments without actual argumentative justification (Just states what rule youve broken instead of telling you why you broke that rule)\n3. Really shitty mods that inconsistently warn individuals without referring the prior cases of offenses and personal bias on behalf of the mods\n 4. Punishments are almost always permanent, the appeal system is nonexistant, making it nearly impossible for people to actually appeal bans and such, and nonetheless, despite what argument you make to moderation it wont matter, even if the argument is logically sound (should add a monthly reset or smth)\n5. The continuous ban of valuable players that would have helped MRTS grow as a whole\n6. Aristocracy created by the upper administration where new mods will only be vetted not on merit, but on personal bias or how well they isolate themselves from the community\n7. Lack of care by the administration to every issue, dmnks in particular isn't professional")
    if message.content.startswith(';poem'):
        await message.channel.send("First they came for the tc3 players, and I did not speak out—because I was not a tc3 player.\n\nThen they came for the people who didn't like dmnk's actions, and I did not speak out—because I did not do that.\n\nThen they came for the staff who disagreed with his methods, and I did not speak out—because I was not staff.\n\nThen they came for me—and there was no one left to speak for me.")

client.run(
    'MTExMjU2MjEzMzI0NzQ1OTQxMQ.GVSG6b.jlFML0AwkcSn6hCIvEj2mC15mdu2vp7PCoKwQ8')
