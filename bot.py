import discord
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv

def run_bot():

    #For secure usage/storage of token.
    load_dotenv()
    TOKEN = os.getenv('discord_token')

    #Specify what events the bot will receive from the gateway.
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    #Facilitates multiple instantiations of the music bot on different servers.
    voice_clients = {}

    #Specifies yt_dlp options.
    ytdl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(ytdl_options)

    #Indicates only audio to be streamed.
    ffmpeg_options = {'options': '-vn'}

    #Is run when the bot becomes online (e.g. After being boot up/rebooted). Indicates is online and ready to use.
    @client.event
    async def on_ready():
        print(f"Bot logged in as {client.user}")

    #Designates the command to play songs on the bot. Ensures the input given is of the correct format.
    @client.event
    async def on_message(msg):
        if msg.content.startswith('?play'):
            try:
                voice_client = await msg.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client

                url = msg.content.split()[1]

                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                song = data['url']
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

                voice_clients[msg.guild.id].play(player)

            except Exception as e:
                print(e)


    client.run(TOKEN)