import discord
import asyncio
import yt_dlp as youtube_dl

# Discord bot Initialization
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Bot token
token = "MTEwMTYzMzMwNjQxMzQ5ODQyOA.GsK-CM.X6DcQbQwqpqysThuSRDPUR2AbWXEvBl1WaPgUE"

voice_clients = {}

# Grabs the best possible audio from yt
yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

# Displays when the bot is online
@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")

# Doesnt diplay video
ffmpeg_options = {'options': "-vn"}



# Joins The channel your in and plays the url
@client.event
async def on_message(msg):
    if msg.content.startswith("?play"):

        try:
            url = msg.content.split()[1]

            # Makes the bot have a voice
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client

            # Grabs the audio data of the url without downloading it
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            # Grabs the data from above and plays it though executable
            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\ffmpeg\\ffmpeg.exe")

            # Plays song
            voice_clients.play(player)

        except Exception as err:
            print(err)

    # Resumes the current song
    if msg.content.startswith('?r'):
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as err:
            print(err)

    # Pauses the current song
    if msg.content.startswith('?p'):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)

    # Deletes the current song
    if msg.content.startswith('?s'):
        try:
            voice_clients[msg.guild.id].disconnect()
        except Exception as err:
            print(err)

# Runs the bot
client.run(token)
