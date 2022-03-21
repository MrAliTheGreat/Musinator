import yt_dlp
import os
from moviepy.editor import VideoFileClip



yt_dlp_options = {
    "format" : "bestvideo[filesize<=6M]+bestaudio[filesize<=2M]",
    "noplaylist" : True
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

def fetchVideo(videoTitle):
    with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
        videoInfo = ydl.extract_info("ytsearch:" + videoTitle, download = True)["entries"][0]
        videoFileName = ydl.prepare_filename(videoInfo)
    return "./" + videoFileName, videoInfo["title"]