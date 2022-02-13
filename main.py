import discord
from discord.ext import commands
import os

musinator = commands.Bot(command_prefix = ".")

@musinator.event
async def on_ready():
  print("Musinator is live!")

@musinator.command()
async def test(ctx):
  await ctx.send("Test Response!")

@musinator.command()
async def join(ctx):
  if(ctx.author.voice):
    await ctx.author.voice.channel.connect()
  else:
    await ctx.send("You are not currently in a channel!")

@musinator.command()
async def leave(ctx):
  if(ctx.voice_client):
    await ctx.voice_client.disconnect()
  else:
    await ctx.send("I'm not in any voice channel!")
  

musinator.run(os.environ["DISCORD_TOKEN"])