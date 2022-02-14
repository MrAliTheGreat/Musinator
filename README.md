# Musinator

Python code of a Discord bot created for playing music in Discord voice chat.

### Commands:

**.test**:
   - Musinator will respond with a sample text --> Sample Response!

**.join**:
   - Musinator will join the voice channel you are currently in
   - If you are not in a voice channel a message is returned pointing it out

**.leave**:
   - Musinator will leave the voice channel it is in
   - If Musinator is not in a voice channel a message is returned pointing it out

**.play [Music Name]**:
   - Musinator will play the song mentioned by the user in the current voice channel

**.pause**:
   - Musinator will pause the song currently playing in the voice channel

**.stop**:
   - Musinator will stop the song currently playing in the voice channel completely
   - By using this command user has to use .play again to play the song that was playing from the start

**.resume**:
   - Musinator will resume the song that was paused