# Musinator

Python code of a Discord bot created for playing music in Discord voice chat.

### Commands:

**-test**:
   - Musinator will respond with a sample text --> Sample Response!

**-join**:
   - Musinator will join the voice channel you are currently in
   - If you are not in a voice channel a message is returned pointing it out

**-leave**:
   - Musinator will leave the voice channel it is in
   - If Musinator is not in a voice channel a message is returned pointing it out

**-play [Music Name]**:
   - Musinator will play the song mentioned by the user in the current voice channel
   - If there is a song playing, the new song will be added to a queue and as soon as the current song ends the first song in the queue will start to play

**-pause**:
   - Musinator will pause the song currently playing in the voice channel

**-skip**:
   - Musinator will stop the song currently playing in the voice channel completely
   - By using this command user has to use .play again to play the song that was playing from the start
   - Also by using this command the song that is currently playing will be skipped and the next song in the queue will be played

**-resume**:
   - Musinator will resume the song that was paused

**-queue**:
   - Musinator will mention all the songs in the queue

**-endingRitual**:
   - Musinator will clear the queue, stop the current song and play Mahtab by Vigen before leaving the voice chat it is in