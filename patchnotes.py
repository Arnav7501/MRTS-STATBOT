from slpp import slpp as lua
import requests


def TableToDict(pastebinURL):
    table = "{" + requests.get(pastebinURL).text[18:-14] + "}"
    table = table.replace("v1.", "")
    table = table.replace("v1", "")
    table = table.replace("\r\n\t--// Buildings //--\r\n\r\n", "")
    return lua.decode(table)


def PrintChanges(old, updated):
    patches = ""
    for thing in old:
        if thing in updated:
            changes = ""
            for attribute in old[thing]:
                changes += checkAttribute(old, updated, thing, attribute)
            if len(changes) > 0:
                patches += f'**{thing}**\n{changes}\n'
        else:
            patches += f'{thing} removed'
    return patches


def checkAttribute(old, updated, thing, attribute):
    changes = ""
    if attribute in updated[thing]:
        if old[thing][attribute] != updated[thing][attribute]:
            sign = old[thing][attribute] - updated[thing][attribute]
            signWord = "changed"
            if sign < 0:
                signWord = "increased"
            else:
                signWord = "decreased"
            changes = f'{attribute} {signWord} {old[thing][attribute]} -> {updated[thing][attribute]}\n'
    else:
        changes = f'{attribute} from {thing} removed'
    return changes