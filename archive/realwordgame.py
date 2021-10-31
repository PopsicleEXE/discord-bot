from discord import reaction, webhook
import requests
import asyncio
from urllib.parse import quote as urlencode
from random import choice,randint
import discord

client = discord.Client()

def randomWebsite():
    response = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=random&format=json&rnnamespace=0&rnlimit=1")
    if response.status_code == 200:
        return str("https://en.wikipedia.org/wiki/"+urlencode(response.json()["query"]["random"][0]["title"],safe=""))
    else:
        return "http://fecalfunny.com"

characters = "qwertyuiopasdfghjklzxcvbnm"

reactions = {
    "✅": True,
    "😳": 'quit',
    "❌": False
}

roundPoints = {}

async def round(msg: discord.Message,checkChars: str,website: str,pageContent: str):
    global roundPoints

    player = msg.author
    channel = msg.channel

    embed = discord.Embed(title='Do you think that "{chars}" appears on the website?'.format(chars=checkChars),description='You have {points} points\n\nReact with ✅ if you think "{chars}" appears on the website\nReact with 😳 if you want to quit and take your points\nReact with ❌ if you think "{chars}" does not appear on the website'.format(chars=checkChars,points=roundPoints[player.id]))
    ourMsg: discord.Message = await channel.send(embed=embed)
    await ourMsg.add_reaction("✅")
    await ourMsg.add_reaction("😳")
    await ourMsg.add_reaction("❌")

    def check(reaction: discord.Reaction,user: discord.User):
        if user.id == player.id and (reaction.emoji == "✅" or reaction.emoji == "😳" or reaction.emoji == "❌"): return True
    try:
        reaction,user = discord.Reaction = await client.wait_for("reaction_add",check=check,timeout=60)
    except asyncio.TimeoutError:
        await channel.send("You didn't respond within one minute.")
        return False,checkChars
    
    action = reactions[reaction.emoji]

    if action == "quit":
        points = roundPoints[player.id]
        if points == 0:
            await channel.send("You quit with no points.")
        if points == 1:
            await channel.send("You quit with 1 point.")
        else:
            await channel.send("You quit with {points} points.".format(points=points))
        return False,checkChars
    elif action == True:
        if pageContent.find(checkChars) > -1:
            await channel.send('"{chars}" was in the website!'.format(chars=checkChars))
            return True,checkChars
        else:
            await channel.send('"{chars}" did not appear on the website.'.format(chars=checkChars))
            await channel.send('The website was {website}'.format(website=website))
            return False,checkChars
    elif action == False:
        if pageContent.find(checkChars) == -1:
            await channel.send('"{chars}" did not appear on the website!'.format(chars=checkChars))
            await channel.send('The website was {website}'.format(website=website))
            return False,checkChars
        else:
            await channel.send('"{chars}" was in the website.'.format(chars=checkChars))
            await channel.send('The website was {website}'.format(website=website))
            return False,checkChars

async def game(msg: discord.Message):
    global websites
    global characters
    global roundPoints

    player = msg.author
    channel = msg.channel

    roundPoints[player.id] = 0

    website = randomWebsite()

    pageContent = requests.get(website).text

    sendCharacters = characters[randint(0,len(characters)-1)]
    while True:
        success,oldChars = await round(msg,sendCharacters,website,pageContent)
        if success == True:
            roundPoints[player.id] = len(oldChars)
            sendCharacters += characters[randint(0,len(characters)-1)]
        elif success == False:
            roundPoints[player.id] = None
            break

@client.event
async def on_message(msg: discord.Message):
    if msg.content == ">wordgame":
        await(game(msg))


client.run("NzgxMzM0MjQ5MjE5MTYyMTIy.X78IOQ.lG7T4QE0PixPnUJHrjR7h90lpPc")