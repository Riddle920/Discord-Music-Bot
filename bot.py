import discord
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv

def run_bot():

    #For secure usage/storage of token
    load_dotenv()
    TOKEN = os.getenv('discord_token')

    #Specify what events the bot will receive from the gateway.
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents)
