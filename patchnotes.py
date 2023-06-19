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
        try:
            if old[thing][attribute] != updated[thing][attribute]:
                match checkInverse(attribute):
                    case 1:
                        changes += f"+ {thing}'s {attribute} changed from {old[thing][attribute]} to {updated[thing][attribute]}\n"
                    case -1:
                        changes += f"- {thing}'s {attribute} changed from {old[thing][attribute]} to {updated[thing][attribute]}\n"
                    case 0:
                        changes += f"\* {thing}'s {attribute} changed from {old[thing][attribute]} to {updated[thing][attribute]}"

        except KeyError as e:
            print(f"KeyError: {e}")
            print(f"x: {thing}, y: {attribute}")
            print(
                f"Keys in old[x]: {old[thing].keys() if thing in old else 'x not in old'}")
            print(
                f"Keys in updated[x]: {updated[thing].keys() if thing in updated else 'x not in updated'}")
    else:
        changes += f"* {attribute} from {thing} removed"

    return changes


def checkInverse(attribute):
    if attribute in inverse:
        return 1
    elif attribute in verse:
        return -1
    else:
        return 0
