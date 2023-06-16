from wikiscraper import scrape_wiki
from discord import Embed


def rankingList():
    singleTargetArray = ["Archer", "Swordman",
                         "Knight", "Longbower", "Crossbower", "Ballista"]

    singleTargetDictionary = {}
    cost = {}
    health = {}
    for i in range(len(singleTargetArray)):
        tempValue = scrape_wiki(singleTargetArray[i])
        cost[tempValue[0]] = tempValue[6]
        health[tempValue[0]] = tempValue[5]
        singleTargetDictionary[tempValue[0]] = tempValue[21]
    sorted_dict = dict(
        sorted(singleTargetDictionary.items(), key=lambda x: x[1]))
    # single Target
    embed = Embed()
    embed.title = "Single Target"
    cost_counter = 0
    print(cost, health)
    for key in sorted_dict:
        costValue = cost[key]
        costValue = costValue.strip('$')
        costHealth = health[key]
        print(key, costValue, costHealth)
        embed.add_field(
            name=key, value="Damage per second: " + sorted_dict[key], inline=False)
        cost_counter += 1
        # + " \nCost effectiveness: " + str(round((float(sorted_dict[key]) / int(costValue) * float(costHealth) * 10), 1)), inline=False
   # await message.channel.send(embed=embed)
    return embed
    splashArray = ["Mage", "Wizard", "Catapult"]
    splashTargetDictionary = {}
    # Splash Target
    # splashCost = []
    # for i in range(len(splashArray)):
    #    tempValue = scrape_wiki(splashArray[i])
    #    splashCost.append(tempValue[6])
    #    splashTargetDictionary[tempValue[0]] = tempValue[23]
   # sorted_dict = dict(
   #     sorted(splashTargetDictionary.items(), key=lambda x: x[1]))
  #  embed = Embed()
  #  embed.title = "Splash Target"
  #  splashCostCounter = 0
  #  for key in sorted_dict:
  # costValue = splashCost[splashCostCounter].strip('$')
 #       embed.add_field(
 #           name=key, value="Damage per second: " + sorted_dict[key] + " \nCost effectiveness: " + str(round((float(sorted_dict[key]) / int(costValue)*100), 1)), inline=False)
 #       splashCostCounter += 1
 #   await message.channel.send(embed=embed)
