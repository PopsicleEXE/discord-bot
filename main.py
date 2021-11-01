PREFIX = ">"
WORK_GAIN = 20

import json
from time import sleep,time
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import quote as urlencode
import random,os
from discord.ext import tasks
import requests
import asyncio
import discord

# this codebase is FUCKED

client: discord.Client = discord.Client()

master_im = Image.open("imposter.jpg")
master_string = "when the imposter is sus!"

y_coord_split = 22

master_x_dict = {
    "w": [[7,29]],
    "h": [[29,43], [83,98]],
    "e": [[43,56], [98,111], [192,205]],
    "n": [[56,69]],
    " ": [[69,75], [111,116], [213,220], [238,244]],
    "t": [[75,83], [183,192]],
    "i": [[116,122], [220,225]],
    "m": [[122,143]],
    "p": [[143,157]],
    "o": [[157,171]],
    "s": [[171,183], [225,238], [244,257], [270,283]],
    "r": [[205,213]],
    "u": [[257,270]],
    "!": [[282,289]],
    "😳": [[289,312]],
}

bootleg_x_dict = {
    "a": [[True, False], [146, 155]],
    "q": [[True, False], [143, 155]],
    "b": [[False, True], [143, 157]],
    "d": [[True, True], [143, 157]],
    "c": [[False, False], [157,167]]
}

characters = "qwertyuiopasdfghjklzxcvbnm"

reactions = {
    "✅": True,
    "😳": 'quit',
    "❌": False
}

roundPoints = {}

master_char_list = list(master_x_dict.keys()) + list(bootleg_x_dict.keys())

def addPoints(player,numPoints):
    newContent = ""
    with open("player.points") as points:
        table = json.loads(points.read())
        if str(player.id) in table:
            table[player.id] = str(int(table[str(player.id)])+numPoints)
            newContent = json.dumps(table)
        else:
            table[player.id] = str(numPoints)
            newContent = json.dumps(table)
        points.close()
    with open("player.points","w") as points:
        points.write(newContent)
        points.close()

async def getSworn(msg):
    with open("times.sworn") as sworn:
        await msg.channel.send(sworn.read())
        sworn.close()

def addSworn():
    times = 0
    with open("times.sworn") as sworn:
        times = int(sworn.read())
        sworn.close()
    with open("times.sworn","w") as sworn:
        sworn.write(str(times+1))
        sworn.close()

def randomWebsite():
    response = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=random&format=json&rnnamespace=0&rnlimit=1")
    if response.status_code == 200:
        return str("https://en.wikipedia.org/wiki/"+urlencode(response.json()["query"]["random"][0]["title"],safe=""))
    else:
        return "http://fecalfunny.com"

async def getIntent(msg):
    split = msg.content.split(" ")
    del split[0]
    string = " ".join(split)

    response = requests.get("https://api.wit.ai/message?v=20211029&q="+urlencode(string,safe=''),headers={'Authorization': "Bearer VFPHAGA34A37HYXPRB7XAABGXSW6LX6N"})
    intent = 'swear'
    highestConfidence = 0
    for intentDict in response.json()['intents']:
        if intentDict['confidence'] > highestConfidence:
            intent = intentDict['name']
            highestConfidence = intentDict['confidence']
    await msg.channel.send(intent)
    if intent == "swear":
        addSworn()

async def sus(msg: discord.Message):
    channel = msg.channel

    split = msg.content.split(" ")
    del split[0]
    input_string = " ".join(split)

    if input_string == "?random": input_string = str(random.randint(1,10))
    if input_string == "?dice": input_string = str(random.randint(1,6))

    location = "jerma-text-slices/"+input_string[:100]+".jpg"

    if os.path.isfile(location):
        await channel.send(file=discord.File(location))
        return

    input_string = input_string.replace(":flushed:", "😳")

    font_path = (os.getcwd() + "/arial.ttf")
    font = ImageFont.truetype(font_path, 13)

    final_image = Image.new('RGB', (len(input_string)*12, master_im.height))

    total_width = 0

    for char in input_string:
        if char in master_x_dict.keys():
            x_coords = random.choice(master_x_dict[char])

            letter = master_im.crop((x_coords[0], 0, x_coords[1], y_coord_split))
            face = master_im.crop((x_coords[0], y_coord_split, x_coords[1], master_im.height))
            
        elif char in bootleg_x_dict.keys():   
            x_coords = bootleg_x_dict[char][1]
            
            letter = master_im.crop((x_coords[0], 0, x_coords[1], y_coord_split))
            face = master_im.crop((x_coords[0], y_coord_split, x_coords[1], master_im.height))

            if bootleg_x_dict[char][0][0]:
                letter = letter.transpose(Image.FLIP_LEFT_RIGHT)
                face = face.transpose(Image.FLIP_LEFT_RIGHT)

            if bootleg_x_dict[char][0][1]:
                letter = letter.transpose(Image.FLIP_TOP_BOTTOM)
                face = face.transpose(Image.FLIP_TOP_BOTTOM)

            if char == "a":
                draw = ImageDraw.Draw(letter)
                draw.rectangle([5, 13, 8, 16], fill=(255,255,255,255))
            
        try:
            random_x = random.randint(0, master_im.width-13)
            scan_line_x_coords = [random_x, random_x+12]
            
            face = master_im.crop((scan_line_x_coords[0], y_coord_split, scan_line_x_coords[1], master_im.height))

            letter = Image.new('RGB', (face.width, y_coord_split))
            draw = ImageDraw.Draw(letter)
            draw.rectangle([0, 0, letter.width, letter.height], fill=(255,255,255,255))
            draw.text((0, 0), char, font=font, fill=(0,0,0,255))
            letter = letter.resize((int(letter.width*1.75), letter.height))
            letter = letter.crop((0, 0, face.width, letter.height))
        except:
            continue

        scan_line = Image.new('RGB', (letter.width, letter.height + face.height))
        scan_line.paste(letter, (0, 0))
        scan_line.paste(face, (0, y_coord_split))
        final_image.paste(scan_line, (total_width, 0))

        total_width += scan_line.width

    final_image.save(location)
    await channel.send(file=discord.File(location))

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

    sendCharacters = characters[random.randint(0,len(characters)-1)]
    while True:
        success,oldChars = await round(msg,sendCharacters,website,pageContent)
        if success == True:
            roundPoints[player.id] = len(oldChars)
            sendCharacters += characters[random.randint(0,len(characters)-1)]
        elif success == False:
            roundPoints[player.id] = None
            break

async def cat(msg: discord.Message):
    for i in range(5):
        cat = requests.get("https://aws.random.cat/meow").json()
        await msg.channel.send(urlencode(cat['file'],safe='/:'))

async def randomLine(msg: discord.Message):
    with open("lines.txt","r") as lines:
        await msg.reply(random.choice(lines.read().split("ඞ")))
        lines.close()

async def zerkOff(msg: discord.message):
    dm = await msg.author.create_dm()
    for i in range(5):
        await dm.send(file=discord.File("jermaZerk.gif"))     

async def help(msg: discord.Message):
    await msg.channel.send(file=discord.File("help.txt"))

async def dice(msg: discord.Message):
    diceCount = max(1,min(100,int(msg.content.split(" ")[1])))
    if not diceCount or type(diceCount) != int:
        diceCount = 1
    if diceCount:
        roll = 0
        for i in range(diceCount):  
            randomRoll = random.randint(1,6)
            if randomRoll == 5 or randomRoll == 6:
                roll -= randomRoll
            else:
                roll += randomRoll
        addPoints(msg.author,roll)
        if roll < 0:
            await msg.reply("you lost "+str(roll*-1)+" points")
        else:
            await msg.reply("you got "+str(roll)+" points")

async def coinFlip(msg: discord.Message):
    bet = int(msg.content.split(" ")[1])
    if bet:
        roll = random.randint(0,1)
        if roll == True:
            addPoints(msg.author,bet)
            await msg.reply("you got "+str(bet)+" points")
        else:
            addPoints(msg.author,-bet)
            await msg.reply("you lost "+str(bet*-1)+" points")

async def debt(msg: discord.Message):
    with open("player.points") as points:
        table = json.loads(points.read())
        if str(msg.author.id) in table:
            debt = int(table[str(msg.author.id)])
            if debt != 0:
                if debt < 0:
                    await msg.channel.send("you are "+str(debt*-1)+" points in debt!")
                else:
                    await msg.channel.send("you have "+str(debt)+" points")
        points.close()

def setCooldown(msg: discord.Message):
    newContent = ""
    with open("work.cooldowns") as cooldowns:
        table = json.loads(cooldowns.read())
        table[msg.author.id] = str(time())
        newContent = json.dumps(table)
        cooldowns.close()
    with open("work.cooldowns","w") as cooldowns:
        cooldowns.write(newContent)
        cooldowns.close()

async def work(msg: discord.Message):
    canWork = False
    with open("work.cooldowns") as cooldowns:
        table = json.loads(cooldowns.read())
        if str(msg.author.id) in table:
            lastTime = int(float(table[str(msg.author.id)]))
            if time()-3600 >= lastTime:
                canWork = True
                setCooldown(msg)
        else:
            canWork = True
            setCooldown(msg)
    if canWork:
        addPoints(msg.author,WORK_GAIN)
        await msg.channel.send("you worked for an hour and gained "+str(WORK_GAIN)+" points.")
    else:
        await msg.channel.send("you need to wait "+str(int(3600-(time()-lastTime)))+" more seconds to work again")

commands = {
    'wordgame': {'command':game,'description':'guess whether or not random combinations of letters appear on a randomly selected wikipedia page','arguments':{}},
    'sussy': {'command':sus,'description':"takes random slices of jerma985's face and makes them a bootleg when the imposter is sus",'arguments': {'string'}},
    'getintent': {'command':getIntent,'description':"uses ai to detect if your input is swearing, and if so adds to the swear counter",'arguments': {'string'}},
    'timessworn': {'command':getSworn,'description':"tells you how many times the ai has evaluated something as swearing in the stinky men server",'arguments':{}},
    'xxx': {'command':zerkOff,'description':"psycho streamer! he zerked off on stream...",'arguments':{}},
    'meow': {'command':cat,'description':"5 cats, free of charge!",'arguments':{}},
    'randomline': {'command':randomLine,'description':"gives you a random line out of 5000 ai-generated lines. sometimes swedish, sometimes japanese, and sometimes javascript, but always random.",'arguments':{}},
    'help': {'command':help,'description':'shows this help message','arguments':{}},
    'dice': {'command':dice,'description':'get 2.5 billion dollars of debt','arguments':{'number of dice'}},
    'coinflip': {'command':coinFlip,'description':'heads, tails, or crippling debt.','arguments':{'bet'}},
    'debt': {'command':debt,'description':'shows you how much debt you have from playing dice. or playing noita.','arguments':{}},
    'work': {'command':work,'description':'work harder, not smarter','arguments':{}}
}

helpMessage = ""
for i,commandName in enumerate(commands):
    command = commands[commandName]
    helpMessage += PREFIX+commandName+': '+command['description']+'\nUsage: '+PREFIX+commandName
    for arg in command['arguments']:
        helpMessage += ' <'+arg+'>'
    if i != len(commands)-1:
        helpMessage += '\n\n'
with open('help.txt','w') as file:
    file.write(helpMessage)
    file.close()

@client.event
async def on_ready():
    print("logged in as "+client.user.name)

@client.event
async def on_message(msg: discord.Message):
    if msg.content.startswith(PREFIX):
        command: str = msg.content.split(" ")[0].replace(PREFIX,"").lower()
        if command:
            if command in commands:
                await commands[command]['command'](msg)

auth = ""
with open("authentication.txt") as authFile:
    auth = authFile.read()

client.run(auth)