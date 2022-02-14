import discord
from discord.ext import commands
import youtube_dl
from dotenv import load_dotenv
import os


load_dotenv()

youtubeDL_options = {
  "format" : "bestaudio/best",
  "noplaylist" : True
}

FFmpeg_options = {
  'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
  'options': '-vn'
}

musinator = commands.Bot(command_prefix = ".")

@musinator.event
async def on_command_error(ctx, error):
  if(isinstance(error, commands.MissingRequiredArgument)):
    await ctx.send("Play What?! Name a song!")

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
    await ctx.send("You are not currently in a voice channel!")

@musinator.command()
async def leave(ctx):
  if(ctx.voice_client):
    await ctx.voice_client.disconnect()
  else:
    await ctx.send("I'm not in any voice channel!")

@musinator.command()
async def play(ctx, *, musicTitle):
  if(not ctx.voice_client):
    await ctx.send("I'm not currently in a voice channel!")
    return
  
  with youtube_dl.YoutubeDL(youtubeDL_options) as ydl:
    info = ydl.extract_info("ytsearch:" + musicTitle, download = False)["entries"][0]
    audioSource = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(info["url"], **FFmpeg_options))
    
    ctx.voice_client.play(audioSource)
    
    await ctx.send("Playing " + info["title"])

@musinator.command()
async def pause(ctx):
  ctx.voice_client.pause()

@musinator.command()
async def stop(ctx):
  ctx.voice_client.stop()

@musinator.command()
async def resume(ctx):
  ctx.voice_client.resume()



musinator.run(os.environ.get("DISCORD_TOKEN"))