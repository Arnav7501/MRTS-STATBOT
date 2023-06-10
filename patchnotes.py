from slpp import slpp as lua
import requests

def TableToDict(pastebinURL):
    table = "{" + requests.get(pastebinURL).text[11:4127] + requests.get(pastebinURL).text[4157:-15] + "}"
    #goofy numbers since first and last 2 lines in pastebin are not relevant and same with 244-246
    return lua.decode(table)

def PrintChanges(old, updated):
    changes = ""
    for x in old:
        for y in x:
            if(old[x][y] != updated[x][y]):
                changes += f"{x} {y} changed from {old[x][y]} to {updated[x][y]}\n"
    return changes