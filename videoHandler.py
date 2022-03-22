import yt_dlp
import os
from moviepy.editor import VideoFileClip


yt_dlp_downloadFilePath = "./video"
webmFileName = "webmVideo"
yt_dlp_options = {
    "format" : "bestvideo[filesize<=6M]+bestaudio[filesize<=2M]",
    "noplaylist" : True,
    "outtmpl" : yt_dlp_downloadFilePath + ".%(ext)s"
}

# Not useful here because gif is much larger in size than the video itself
# Also there is a 8 MB file size limit on Discord
# But I'll leave it here. Maybe in the future it will come in handy!
def convertVideoToGif(videoPath):
    print("Converting Video to GIF...")
    video = VideoFileClip(videoPath)
    video.write_gif("./gifVersion.gif")
    
    print("Removing Video Source...")
    os.remove(videoPath)

    return "./gifVersion.gif"

# -crf can be changed to 55 just to be sure filesize won't go past 8MB
def convertToWebM(videoPath):
    os.system('ffmpeg -i "' + videoPath + '" -c:v libvpx -b:v 0 -crf 50 "' + webmFileName + '.webm"')
    os.remove(videoPath)
    return "./" + webmFileName + ".webm"

def fetchVideo(videoTitle):
    with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
        videoInfo = ydl.extract_info("ytsearch:" + videoTitle, download = True)["entries"][0]
    
    if(os.path.isfile(yt_dlp_downloadFilePath + '.mkv')):
        return yt_dlp_downloadFilePath + '.mkv', videoInfo["title"]
    
    elif(os.path.isfile(yt_dlp_downloadFilePath + '.mp4')):
        return yt_dlp_downloadFilePath + '.mp4', videoInfo["title"]
    
    return yt_dlp_downloadFilePath + '.webm', videoInfo["title"] 
