import discord
from discord import app_commands
from discord.ext import commands
import os
import requests
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_ENDPOINT = os.getenv("API_ENDPOINT")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="uploadsong", description="Upload custom lagu ke GDPS-mu")
@app_commands.describe(title="Judul lagu", author="Pembuat lagu", youtube_url="(opsional) URL YouTube")
async def uploadsong(interaction: discord.Interaction, title: str, author: str, youtube_url: str = "None"):
    song_id = random.randint(100000, 999999)
    uploader = str(interaction.user)
    gdps_link = f"https://fless.ps.fhgdps.com/song/{song_id}"

    data = {
        "song_id": song_id,
        "title": title,
        "author": author,
        "youtube_url": youtube_url,
        "uploader": uploader,
        "gdps_link": gdps_link
    }

    try:
        response = requests.post(API_ENDPOINT, data=data)
        if response.status_code == 200:
            await interaction.response.send_message(f"Lagu berhasil diupload!
**{title}** by **{author}**
[GDPS Link]({gdps_link})", ephemeral=True)
        else:
            await interaction.response.send_message("Gagal upload ke website.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}", ephemeral=True)

bot.run(TOKEN)