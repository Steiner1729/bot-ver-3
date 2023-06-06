import discord
from discord.ext import commands
import youtube_dl

# Discord bot token
with open('./token', 'r') as f:
    TOKEN = f.read()
    # TOKEN = 'MTEwNzIxMDkwMjAzMTMwNjgxMw.G9wKNf.354sY2bvnSVVjIPBTzHlFYeAbQkyyhc9QcjXEI'

# Create a Discord bot instance
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def play(ctx, url):
    # Check if the user is in a voice channel
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("You need to join a voice channel first.")
        return

    # Join the voice channel
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    # Download audio from YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2)

    # Play audio
    voice_client.play(source)
    await ctx.send(f'Now playing: {info["title"]}')

@bot.command()
async def stop(ctx):
    # Check if the bot is in a voice channel
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send('Bot disconnected')

# Run the bot
bot.run(TOKEN)
