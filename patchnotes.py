from slpp import slpp as lua
import requests

inverse = {"Damage", "MaxHealth", "Range", "Speed", "SplashRange", "AddHealth", "AddBuildings", "GiveCash", "AddUnits"}
verse = {"Cost", "Space", "Time", "Rate"}

def TableToDict(pastebinURL):
    table = "{" + requests.get(pastebinURL).text[18:-14] + "}"
    table = table.replace("v1.", "")
    table = table.replace("v1", "")
    table = table.replace("\r\n\t--// Buildings //--\r\n\r\n", "")

    # goofy numbers since first and last 2 lines in pastebin are not relevant and same with 244-246
    return lua.decode(table)


def PrintChanges(old, updated):
    changes = ""
    for thing in old:
        if thing in updated:
            for attribute in old[thing]:
                changes += checkAttribute(old, updated, thing, attribute)
        else:
            changes += f"* {thing} removed\n"
    return changes

def checkAttribute(old, updated, thing, attribute):
    changes = ""
    if attribute in updated[thing]:
        if old[thing][attribute] != updated[thing][attribute]:
            changes += f"{isGood(attribute, old[thing][attribute], new[thing][attribute])} {thing}'s {attribute} changed from {old[thing][attribute]} to {updated[thing][attribute]}\n"
    else:
        changes += f"* {attribute} from {thing} removed"
    return changes

def isGood(attribute, old, new):
    sign = ""
    if new > old:
        if attribute in inverse:
            sign = "+"
        elif attribute in verse:
            sign = "-"
        else:
            sign = "\*"
    else:
        if attribute in inverse:
            sign = "-"
        elif attribute in verse:
            sign = "+"
        else:
            sign = "\*"
    return sign