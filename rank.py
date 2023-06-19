from wikiscraper import scrape_wiki
from discord import Embed
import patchnotes


def rankingList(type):
    singleTargetArray = ["Archer", "Swordman",
                         "Knight", "Longbower", "Crossbower", "Ballista"]

    singleTargetDictionary = {}
    table = patchnotes.TableToDict(
        "https://pastebin.com/raw/xchHf3Gp")
    for item in singleTargetArray:
        if type == "dps":
            singleTargetDictionary[item] = round(float(table[item]["Damage"] /
                                                       table[item]["Rate"]), 2)
        if type == "health":
            singleTargetDictionary[item] = table[item]["MaxHealth"]
        if type == "speed":
            singleTargetDictionary[item] = table[item]["Speed"]
    sorted_dict = dict(
        sorted(singleTargetDictionary.items(), key=lambda x: x[1]))
    # single Target
    embed = Embed()
    embed.title = "Single Target"
    for key in sorted_dict:
        embed.add_field(
            name=key, value=f"{type}: " + str(sorted_dict[key]), inline=False)
    return embed


def splashRankingList(type):
    splashArray = ["Wizard", "Catapult"]
    splashTargetDictionary = {}
    table = patchnotes.TableToDict(
        "https://pastebin.com/raw/xchHf3Gp")
    for item in splashArray:
        if type == "dps":
            splashTargetDictionary[item] = round(float(table[item]["Damage"] /
                                                       table[item]["Rate"]), 2)
        if type == "health":
            splashTargetDictionary[item] = table[item]["MaxHealth"]
        if type == "speed":
            splashTargetDictionary[item] = table[item]["Speed"]

    sorted_dict = dict(
        sorted(splashTargetDictionary.items(), key=lambda x: x[1]))
    embed = Embed()
    embed.title = "Splash Target"
    for key in sorted_dict:
        embed.add_field(
            name=key, value=f"{type} " + str(sorted_dict[key]), inline=False)
    return embed
