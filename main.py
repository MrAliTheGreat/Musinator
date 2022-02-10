import discord
import os

client = discord.Client()

@client.event
async def on_ready():
  print("Musinator is live!")


@client.event
async def on_message(message):
  if(message.author is client.user):
    return

  if(message.content.startswith("-test")):
    await message.channel.send("I'm OK!")


client.run(os.environ["DISCORD_TOKEN"]) # Environment Variable is on repl.it