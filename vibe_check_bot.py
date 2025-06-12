import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Spotify API Auth
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

# Mood-to-Spotify-Query map
MOOD_QUERIES = {
    'sad': ['melancholy', 'sad songs', 'acoustic heartbreak', 'lonely', 'slow chill'],
    'hype': ['party', 'workout', 'hype hits', 'motivational', 'energy boost'],
    'romantic': ['love songs', 'romantic hits', 'soft pop'],
    'chill': ['chill vibes', 'lofi', 'ambient'],
    'angry': ['metal', 'hard rock', 'rage playlist'],
    'happy': ['feel good', 'sunny day', 'good vibes']
}

@bot.event
async def on_ready():
    print(f'🎧 Vibe Check Bot is online as {bot.user}')

@bot.command(name='vibe')
async def vibe(ctx, mood: str):
    mood = mood.lower()
    if mood not in MOOD_QUERIES:
        await ctx.send("😕 I don't know that mood. Try one of: " + ", ".join(MOOD_QUERIES.keys()))
        return

    query = random.choice(MOOD_QUERIES[mood])
    results = spotify.search(q=query, type='track', limit=10)
    tracks = results['tracks']['items']

    if not tracks:
        await ctx.send("😢 I couldn't find any songs for that mood.")
        return

    track = random.choice(tracks)
    name = track['name']
    artist = track['artists'][0]['name']
    url = track['external_urls']['spotify']

    await ctx.send(f"🎶 **{name}** – *{artist}* (Mood: {mood.capitalize()})\n{url}")

# Run the bot
bot.run(DISCORD_TOKEN)
