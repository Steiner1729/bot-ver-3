import discord
from discord.ext import commands
import youtube_dl
import os

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Event for when the bot is ready
@bot.event
async def on_ready():
    print("BOT READY.")


# Command to play music
@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    # Check if the bot is already in a voice channel
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()

    # Connect to the voice channel
    vc = await voice_channel.connect()

    # Download the audio from YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(id)s.%(ext)s',
        'verbose' : True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        ydl.download([url])

    # Play the audio
    vc.play(discord.FFmpegPCMAudio(f"{info['id']}.mp3"))

# Run the bot
bot.run('MTEwNzIxMDkwMjAzMTMwNjgxMw.Ge_0d-.Lht0fwImeIqi2IvbEqvAkvyj8F8WmKzy7Hz-Ag')
