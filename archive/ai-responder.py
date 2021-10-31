import discord
from re import sub
from time import sleep
from random import choice
from transformers import GPT2LMHeadModel, GPT2Tokenizer

starterWords = ["one ","the ","it ","a ","when ","why ","who ","how ","what "]

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

client = discord.Client()

def addWord(string):
  inputs = tokenizer.encode(string,return_tensors='pt')
  output = model.generate(inputs,max_length=(len(string)/3)+5,do_sample=True)
  return tokenizer.decode(output[0],skip_special_tokens=True)

@client.event
async def on_ready():
  channel = client.get_channel(850513218405400687)
  await channel.send(choice(starterWords))

@client.event
async def on_message(msg: discord.Message):
  if msg.author.id == 718906488285823057 or (msg.content.startswith("test") and msg.author.id != client.user.id):
    longerMsg = addWord(msg.content)
    if len(longerMsg) < 2000:
      sleep(.6)
      await msg.reply(sub("\n"," ",longerMsg))
    else:
      await msg.reply(choice(starterWords))


client.run("NzgxMzM0MjQ5MjE5MTYyMTIy.X78IOQ.lG7T4QE0PixPnUJHrjR7h90lpPc")