from main import client
channelid = "None"
def setChannel(id):
    if channelid.lower() == "none":
        channelid = "None"
    else:
        channelid = id
    return f"Channel set to {channelid}"

def sendLog(content):
    if channelid != "None":
        embed1 = embed()
        embed2 = embed()
        if content[0] == "elo":
            user1 = client.get_user(content[1])
            user2 = client.get_user(content[4])
            embed1.setauthor(f'<@{content[1]}>', f'https://cdn.discordapp.com/avatars/{user1["id"]}/{user1["avatar"]}.png')
            embed1.settitle(f'{content[1]} -> {content[2]}')
            embed1.setdescription(f'Change in elo: {content[3] - content[2]}')
        client.get_channel(channelid).send(f'Elo Change {embed}')