import discord
from pytube import YouTube
import os
import re
import json
from datetime import datetime

# Setup intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = discord.Client(intents=intents)

# Folder dan file penyimpanan
DOWNLOAD_FOLDER = "downloads"
DB_FILE = "songs.json"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

MAX_FILE_SIZE_MB = 8  # Batas upload Discord

def convert_size(size_bytes):
    return round(size_bytes / (1024 * 1024), 2)

def save_song(data):
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            all_data = json.load(f)
    else:
        all_data = []

    all_data.append(data)

    with open(DB_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    if message.mentions and bot.user in message.mentions:
        # Command: reup
        if "reup" in content:
            match = re.search(r'(https?://\S+)', message.content)
            if not match:
                await message.channel.send("URL YouTube tidak ditemukan.")
                return

            url = match.group(1)
            await message.channel.send("Mengunduh lagu, tunggu sebentar...")

            try:
                yt = YouTube(url)
                title = yt.title
                stream = yt.streams.filter(only_audio=True).first()
                file_path = stream.download(output_path=DOWNLOAD_FOLDER)
                base, _ = os.path.splitext(file_path)
                new_file = base + ".mp3"
                os.rename(file_path, new_file)

                size_mb = convert_size(os.path.getsize(new_file))
                if size_mb > MAX_FILE_SIZE_MB:
                    await message.channel.send(f"Gagal upload: File terlalu besar ({size_mb} MB).")
                    os.remove(new_file)
                    return

                await message.channel.send(content=f"**{title}**", file=discord.File(new_file))

                # Simpan ke songs.json
                save_song({
                    "judul": title,
                    "url": url,
                    "uploader": str(message.author),
                    "tanggal": str(datetime.utcnow()),
                })

                os.remove(new_file)

            except Exception as e:
                await message.channel.send(f"Gagal upload lagu: {e}")

        # Command: info
        elif "info" in content:
            try:
                parts = message.content.split("info", 1)[1].strip().split("|")
                if len(parts) < 2:
                    await message.channel.send("Format: `@Bot info Judul | Artis | [Tahun]`")
                    return

                title = parts[0].strip()
                artist = parts[1].strip()
                year = parts[2].strip() if len(parts) > 2 else "Unknown"

                await message.channel.send(
                    f"**Judul:** {title}\n**Artis:** {artist}\n**Tahun:** {year}"
                )
            except:
                await message.channel.send("Gagal memproses info.")

import os
bot.run(os.getenv("BOT_TOKEN"))
