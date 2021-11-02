PREFIX = ">"
WORK_GAIN = 20
MIN_STOCK = 0.05

import yfinance
import json
from time import time
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

roundDollars = {}

master_char_list = list(master_x_dict.keys()) + list(bootleg_x_dict.keys())

def getDollars(player):
    with open("player.dollars") as dollars:
        table = json.loads(dollars.read())
        dollars.close()
        if str(player.id) in table:
            return float(table[str(player.id)])
        else:
            return 0

def addDollars(player,numDollars):
    newContent = ""
    with open("player.dollars") as dollars:
        table = json.loads(dollars.read())
        if str(player.id) in table:
            table[player.id] = str(float(table[str(player.id)])+numDollars)
            newContent = json.dumps(table)
        else:
            table[player.id] = str(numDollars)
            newContent = json.dumps(table)
        dollars.close()
    with open("player.dollars","w") as dollars:
        dollars.write(newContent)
        dollars.close()

def addStocks(player,symbol,shares):
    newContent = ""
    with open("player.stocks") as stocks:
        table = json.loads(stocks.read())
        if str(player.id) in table:
            playerTable = table[str(player.id)]
            if symbol in playerTable:
                playerTable[symbol] += shares
            else:
                table[str(player.id)][symbol] = shares
            newContent = json.dumps(table)
        else:
            table[str(player.id)] = {symbol: str(shares)}
            newContent = json.dumps(table)
        stocks.close()
    with open("player.stocks","w") as stocks:
        stocks.write(newContent)
        stocks.close()

def getShares(player,symbol):
    with open("player.stocks") as stocks:
        table = json.loads(stocks.read())
        if str(player.id) in table:
            playerTable = table[str(player.id)]
            if symbol in playerTable:
                return playerTable[symbol]

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
    global roundDollars

    player = msg.author
    channel = msg.channel

    embed = discord.Embed(title='Do you think that "{chars}" appears on the website?'.format(chars=checkChars),description='You have {dollars} dollars\n\nReact with ✅ if you think "{chars}" appears on the website\nReact with 😳 if you want to quit and take your dollars\nReact with ❌ if you think "{chars}" does not appear on the website'.format(chars=checkChars,dollars=roundDollars[player.id]))
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
        dollars = roundDollars[player.id]
        if dollars == 0:
            await channel.send("You quit with no dollars.")
        if dollars == 1:
            await channel.send("You quit with 1 dollar.")
        else:
            await channel.send("You quit with {dollars} dollars.".format(dollars=dollars))
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
    global roundDollars

    player = msg.author
    channel = msg.channel

    roundDollars[player.id] = 0

    website = randomWebsite()

    pageContent = requests.get(website).text

    sendCharacters = characters[random.randint(0,len(characters)-1)]
    while True:
        success,oldChars = await round(msg,sendCharacters,website,pageContent)
        if success == True:
            roundDollars[player.id] = len(oldChars)
            sendCharacters += characters[random.randint(0,len(characters)-1)]
        elif success == False:
            roundDollars[player.id] = None
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
    diceCount = min(100,int(msg.content.split(" ")[1]))
    if not diceCount or type(diceCount) != int:
        diceCount = 1
    if getDollars(msg.author) >= float(6*diceCount):
        roll = 0
        for i in range(diceCount):  
            randomRoll = random.randint(1,6)
            if randomRoll == 5 or randomRoll == 6:
                roll -= randomRoll
            else:
                roll += randomRoll
        addDollars(msg.author,float(roll))
        if roll < 0:
            await msg.reply("you lost "+str(roll*-1)+" dollars")
        else:
            await msg.reply("you got "+str(roll)+" dollars")
    else:
        await msg.reply("you don't have enough dollars to do this")

async def coinFlip(msg: discord.Message):
    bet = float(msg.content.split(" ")[1])
    if type(bet) != float or not bet > 0:
        bet = 10
    if getDollars(msg.author) >= bet:
        roll = random.randint(0,1)
        if roll == True:
            addDollars(msg.author,bet)
            await msg.reply("you got "+str(bet)+" dollars")
        else:
            addDollars(msg.author,-bet)
            await msg.reply("you lost "+str(bet)+" dollars")
    else:
        await msg.reply("you don't have enough dollars to do this")

async def debt(msg: discord.Message):
    with open("player.dollars") as dollars:
        table = json.loads(dollars.read())
        if str(msg.author.id) in table:
            debt = float(table[str(msg.author.id)])
            if debt != 0:
                if debt < -1:
                    await msg.channel.send("you are "+str(debt*-1)+" dollars in debt!")
                elif debt > 1:
                    await msg.channel.send("you have "+str(debt)+" dollars")
                elif debt == 1:
                    await msg.channel.send("you have 1 dollar")
                elif debt == -1:
                    await msg.channel.send("you are 1 dollar in debt")
            else:
                await msg.channel.send("you have no dollars")
        else:
            await msg.channel.send("you have no dollars")
        dollars.close()

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
        addDollars(msg.author,WORK_GAIN)
        await msg.channel.send("you worked for an hour and gained "+str(WORK_GAIN)+" dollars.")
    else:
        await msg.channel.send("you need to wait "+str(int(3600-(time()-lastTime)))+" more seconds to work again")

async def buyStock(msg: discord.Message):
    split = msg.content.split(" ")
    symbol = split[1].lower()
    shares = float(split[2])
    if symbol and shares:
        info = yfinance.Ticker(symbol).info
        if "currentPrice" in info:
            if shares >= MIN_STOCK:
                price = info["currentPrice"]*shares
                if price > getDollars(msg.author):
                    await msg.reply("you don't have enough money to buy that stock; it would cost $"+str(price)+" and you have $"+str(getDollars(msg.author)));
                    return
                if shares == 1:
                    ourMsg = await msg.reply("are you sure you want to buy 1 share of "+symbol+" stock? this will cost you $"+str(price))
                else:
                    ourMsg = await msg.reply("are you sure you want to buy "+str(shares)+" shares of "+symbol+" stock? this will cost you $"+str(price))
                await ourMsg.add_reaction("✅")
                await ourMsg.add_reaction("❌")
                def check(reaction: discord.Reaction,user: discord.User):
                    if user.id == msg.author.id and (reaction.emoji == "✅" or reaction.emoji == "❌"): return True
                try:
                    reaction,user = discord.Reaction = await client.wait_for("reaction_add",check=check,timeout=60)
                except asyncio.TimeoutError:
                    await msg.reply("you didn't respond within one minute.")
                    return
                reaction = reactions[reaction.emoji]
                print(reaction)
                if reaction == True:
                    addStocks(msg.author,symbol,shares)
                    addDollars(msg.author,-price)
                    if shares == 1:
                        await msg.reply("transaction complete! you purchased 1 share of "+symbol+" stock")
                    else:
                        await msg.reply("transaction complete! you purchased "+str(shares)+" shares of "+symbol+" stock")
                else:
                    await msg.reply("transaction cancelled")
            else:
                await msg.reply("the minimum number of shares you can buy is "+str(MIN_STOCK))
        else:
            await msg.reply("invalid symbol")
    else:
        await msg.reply("incorrect arguments, check "+PREFIX+"help")

async def viewStock(msg: discord.Message):
    symbol = msg.content.split(" ")[1]
    if symbol:
        info = yfinance.Ticker(symbol).info
        if "currentPrice" in info:
            price = info["currentPrice"]
            message = symbol+" is currently worth $"+str(price)
            shares = getShares(msg.author,symbol)
            if shares:
                if shares == 1:
                    message += "\nyou have 1 share, worth $"+str(price)
                else:
                    print(type(shares),type(price))
                    message += "\nyou have "+str(shares)+" shares, worth $"+str(shares*price)
            await msg.reply(message)
        else:
            await msg.reply("invalid symbol")
    else:
        await msg.reply("incorrect arguments, check "+PREFIX+"help")

async def sellStock(msg: discord.Message):
    split = msg.content.split(" ")
    symbol = split[1]
    shares = float(split[2])

    if symbol and shares:
        info = yfinance.Ticker(symbol).info
        if "currentPrice" in info:
            ownedShares = getShares(msg.author,symbol)
            price = info["currentPrice"]*shares
            if ownedShares:
                if shares > 0:
                    if ownedShares >= shares:
                        if shares == 1:
                            ourMsg = await msg.reply("are you sure you want to sell 1 share of "+symbol+" stock? this will give you $"+str(price))
                        else:
                            ourMsg = await msg.reply("are you sure you want to sell "+str(shares)+" shares of "+symbol+" stock? this will give you $"+str(price))
                        await ourMsg.add_reaction("✅")
                        await ourMsg.add_reaction("❌")
                        def check(reaction: discord.Reaction,user: discord.User):
                            if user.id == msg.author.id and (reaction.emoji == "✅" or reaction.emoji == "❌"): return True
                        try:
                            reaction,user = discord.Reaction = await client.wait_for("reaction_add",check=check,timeout=60)
                        except asyncio.TimeoutError:
                            await msg.reply("you didn't respond within one minute.")
                            return
                        reaction = reactions[reaction.emoji]
                        print(reaction)
                        if reaction == True:
                            addStocks(msg.author,symbol,-shares)
                            addDollars(msg.author,-price)
                            if shares == 1:
                                await msg.reply("transaction complete! you sold 1 share of "+symbol+" stock")
                            else:
                                await msg.reply("transaction complete! you sold "+str(shares)+" shares of "+symbol+" stock")
                        else:
                            await msg.reply("transaction cancelled")
                    else:
                        await msg.reply("you don't own that many shares")
                else:
                    await msg.reply("you cannot sell "+shares+" shares")
            else:
                await msg.reply("you don't own any of that stock")
        else:
            await msg.replt("invalid symbol")
    else:
        await msg.reply("incorrect arguments, check "+PREFIX+"help")

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
    'work': {'command':work,'description':'work harder, not smarter','arguments':{}},
    'buystock': {'command':buyStock,'description':'stonk','arguments':{'symbol','shares'}},
    'viewstock': {'command':viewStock,'description':'view the value of a stock and the value of your shares in it','arguments':{'symbol'}},
    'sellstock': {'command':sellStock,'description':'guess what this does','arguments':{'symbol','shares'}}
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