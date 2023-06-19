from slpp import slpp as lua
import requests


def TableToDict(pastebinURL):
    table = "{" + requests.get(pastebinURL).text[17:-14] + "}"
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
                try:
                    if old[thing][attribute] != updated[thing][attribute]:
                        changes += f"{thing}'s {attribute} changed from {old[thing][attribute]} to {updated[thing][attribute]}\n"
                except KeyError as e:
                    print(f"KeyError: {e}")
                    print(f"x: {thing}, y: {attribute}")
                    print(
                        f"Keys in old[x]: {old[thing].keys() if thing in old else 'x not in old'}")
                    print(
                        f"Keys in updated[x]: {updated[thing].keys() if thing in updated else 'x not in updated'}")
        else:
            changes += f"{thing} removed\n"
    return changes
