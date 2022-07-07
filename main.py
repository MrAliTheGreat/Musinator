import asyncio
import discord
from discord.ext import commands
import youtube_dl
from dotenv import load_dotenv
import os

from videoHandler import convertToWebM, fetchVideo


load_dotenv()

song_queue = []

youtubeDL_options = {
  "format" : "bestaudio/best",
  "noplaylist" : True
}

FFmpeg_options = {
  'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
  'options': '-vn'
}

musinator = commands.Bot(command_prefix = "-")


def convertToTimeFormat(seconds):
  minutes = str(seconds // 60)
  remainingSeconds = str(seconds % 60)
  if(len(remainingSeconds) == 1):
    remainingSeconds = "0" + remainingSeconds
  return minutes + ":" + remainingSeconds

def playNextSongInQueue(ctx):
  if(len(song_queue) > 0):
    ctx.voice_client.play(song_queue[0][0], after = lambda _ : playNextSongInQueue(ctx))
    asyncio.run_coroutine_threadsafe(
      ctx.send("Now Playing " + song_queue[0][1] + "   |   Duration: " + convertToTimeFormat(song_queue[0][2])),
      musinator.loop
    )
    del song_queue[0]

def getAudio(musicTitle):
  with youtube_dl.YoutubeDL(youtubeDL_options) as ydl:
    info = ydl.extract_info("ytsearch:" + musicTitle, download = False)["entries"][0]
    audioSource = discord.PCMVolumeTransformer(
      discord.FFmpegPCMAudio(
        source = info["url"], **FFmpeg_options
      )
    )
  
  return audioSource, info


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
    song_queue.clear()
  else:
    await ctx.send("I'm not in any voice channel!")

@musinator.command()
async def play(ctx, *, musicTitle):
  if(not ctx.voice_client):
    await ctx.send("I'm not currently in a voice channel!")
    return

  audioSource, info = getAudio(musicTitle)

  if(ctx.voice_client.is_playing() or len(song_queue) > 0):
    song_queue.append([ audioSource, info["title"], info["duration"] ])
    await ctx.send("Song " + info["title"] + " was added to the queue")
    return
  
  ctx.voice_client.play(audioSource, after = lambda _ : playNextSongInQueue(ctx))
  await ctx.send("Playing " + info["title"] + "  |   Duration: " + convertToTimeFormat(info["duration"]) )

@musinator.command()
async def queue(ctx):
  if(len(song_queue) == 0):
    await ctx.send("There is no song in the queue!")
    return

  await ctx.send("Songs in queue: ")
  for _, title, duration in song_queue:
    await ctx.send(title + "   |   " + convertToTimeFormat(duration) )

@musinator.command()
async def endingRitual(ctx):
  if(not ctx.voice_client):
    await ctx.send("I'm not currently in a voice channel!")
    return

  audioSource, info = getAudio("Mahtab Vigen")

  song_queue.clear()
  if(ctx.voice_client.is_playing()):
    ctx.voice_client.stop()
  
  ctx.voice_client.play(
    audioSource,
    after = lambda _ : asyncio.run_coroutine_threadsafe(
      ctx.voice_client.disconnect(),
      musinator.loop
    )
  )
  await ctx.send(
    "Cleared The Queue\n" + 
    "Playing " + info["title"] + "  |   Duration: " + convertToTimeFormat(info["duration"]) + "\n"
    "Before Ending The Call!"
  )

@musinator.command()
async def video(ctx, *, videoTitle):
  videoPath, videoName = fetchVideo(videoTitle)
  await ctx.send(
    "Video Downloaded!"
  )
  if(videoPath[-4:] != "webm"):
    await ctx.send(
      "Converting to WebM..."
    )
    videoPath = convertToWebM(videoPath)
    await ctx.send(
      "WebM Created!"
    )
  await ctx.send(
    "Uploading to Discord..."
  )
  await ctx.send(
    "-----  " + videoName + "  -----",
    file = discord.File(videoPath)
  )
  os.remove(videoPath)

@musinator.command()
async def listen(ctx):
  # TO DO
  # As of right now discord.py does not support receiving audio!
  pass

@musinator.command()
async def pause(ctx):
  ctx.voice_client.pause()

@musinator.command()
async def skip(ctx):
  ctx.voice_client.stop()

@musinator.command()
async def resume(ctx):
  ctx.voice_client.resume()
  


musinator.run(os.environ.get("DISCORD_TOKEN"))