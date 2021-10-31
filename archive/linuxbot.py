import random
import discord
from threading import Thread as thread
from discord.ext import tasks
from transformers import GPT2LMHeadModel, GPT2Tokenizer

starterWords = ["one ","the ","it ","a ","when ","why ","who ","how ","what "]

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

client = discord.Client()

@client.event
async def on_message(msg: discord.Message):
  if msg.content == ">random":
    with open("lines.txt","r") as lines:
      await msg.reply(random.choice(lines.read().split("ඞ")))

client.run("NzgxMzM0MjQ5MjE5MTYyMTIy.X78IOQ.lG7T4QE0PixPnUJHrjR7h90lpPc")