import discord
import requests
from urllib.parse import quote as urlEncode
from difflib import SequenceMatcher
from re import sub

client = discord.Client()

swears = ['bitch','ass','fuck','dick','damn','hell','retard','faggot','fag','die','idiot','dumb','noob','shit','piss','cum']
sussySwears = ['suspicious','sus','among us','amogus','fecalfunny.com','fecalfunny','bad','robot','bot','among','texas','massachussets','coolpixels','stinky','1cool','keyboard',]

def getSworn():
    with open("times.sworn") as sworn:
        read = sworn.read()
        sworn.close()
        return int(read)
def addSworn():
    times = 0
    with open("times.sworn") as sworn:
        times = int(sworn.read())
        sworn.close()
    with open("times.sworn","w") as sworn:
        sworn.write(str(times+1))
        sworn.close()

def getCensor(length):
    out = ""
    for i in range(length):
        out += "🤍"
    return out

def getIntent(string):
    response = requests.get("https://api.wit.ai/message?v=20211029&q="+urlEncode(string,safe=''),headers={'Authorization': "Bearer VFPHAGA34A37HYXPRB7XAABGXSW6LX6N"})
    intent = 'swear'
    highestConfidence = 0
    for intentDict in response.json()['intents']:
        if intentDict['confidence'] > highestConfidence:
            intent = intentDict['name']
            highestConfidence = intentDict['confidence']
    return intent

@client.event
async def on_message(msg: discord.Message):
    if msg.author.bot == False and msg.type == discord.MessageType.default and type(msg.content) == str:
        await msg.channel.send(getIntent(msg.content))

client.run("NzgxMzM0MjQ5MjE5MTYyMTIy.X78IOQ.lG7T4QE0PixPnUJHrjR7h90lpPc")