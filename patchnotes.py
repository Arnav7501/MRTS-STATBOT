from slpp import slpp as lua
import requests

inverse = {"Damage", "MaxHealth", "Range", "Speed", "SplashRange",
           "AddHealth", "AddBuildings", "GiveCash", "AddUnits"}
verse = {"Cost", "Space", "Time", "Rate"}


def TableToDict(pastebinURL):
    table = "{" + requests.get(pastebinURL).text[18:-14] + "}"
    table = table.replace("v1.", "")
    table = table.replace("v1", "")
    table = table.replace("\r\n\t--// Buildings //--\r\n\r\n", "")
    return lua.decode(table)


def PrintChanges(old, updated):
    changes = ""
    for thing in old:
        if thing in updated:
            for attribute in old[thing]:
                changes += checkAttribute(old, updated, thing, attribute)
        else:
            changes += f"* {thing} removed\n"
    if len(changes) > 0:
        changes = "```" + changes + "```"
    return changes


def checkAttribute(old, updated, thing, attribute):
    changes = ""
    if attribute in updated[thing]:
        if old[thing][attribute] != updated[thing][attribute]:
            sign = isGood(attribute, old[thing][attribute], updated[thing][attribute])
            signWord = "changed"
            match sign:
                case "+":
                    signWord = "increased"
                case "-":
                    signWord = "decreased"
            changes += f"{sign} {thing}'s {attribute} {signWord} from {old[thing][attribute]} to {updated[thing][attribute]}\n"
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