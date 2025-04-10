import discord
from pytube import YouTube
import os
import re
import json
from datetime import datetime
from moviepy.editor import AudioFileClip

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = discord.Client(intents=intents)

# Folder & File
DOWNLOAD_FOLDER = "downloads"
DB_FILE = "songs.json"
MAX_FILE_SIZE_MB = 8

# Cek dan buat folder
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Save data lagu
def save_song(data):
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            all_data = json.load(f)
    else:
        all_data = []
    all_data.append(data)
    with open(DB_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

def convert_size(size_bytes):
    return round(size_bytes / (1024 * 1024), 2)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    if message.mentions and bot.user in message.mentions:
        # Reup Command
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
                temp_path = stream.download(output_path=DOWNLOAD_FOLDER)
                base, _ = os.path.splitext(temp_path)
                mp3_path = base + ".mp3"

                # Convert ke MP3 asli
                clip = AudioFileClip(temp_path)
                clip.write_audiofile(mp3_path, verbose=False, logger=None)
                clip.close()
                os.remove(temp_path)

                size_mb = convert_size(os.path.getsize(mp3_path))
                if size_mb > MAX_FILE_SIZE_MB:
                    await message.channel.send(f"Gagal upload: File terlalu besar ({size_mb} MB).")
                    os.remove(mp3_path)
                    return

                await message.channel.send(content=f"**{title}**", file=discord.File(mp3_path))

                save_song({
                    "judul": title,
                    "url": url,
                    "uploader": str(message.author),
                    "tanggal": str(datetime.utcnow())
                })

                os.remove(mp3_path)

            except Exception as e:
                await message.channel.send(f"Gagal upload lagu: {e}")

        # Info Command
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
