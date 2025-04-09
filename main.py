import discord
from pytube import YouTube
import os
import re

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # penting untuk membaca isi pesan

bot = discord.Client(intents=intents)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Format: @FlessSongID reup <url>
    if message.mentions and bot.user in message.mentions and "reup" in message.content:
        match = re.search(r'(https?://\S+)', message.content)
        if not match:
            await message.channel.send("URL YouTube tidak ditemukan.")
            return

        url = match.group(1)
        await message.channel.send("Mengunduh lagu, tunggu sebentar...")

        try:
            yt = YouTube(url)
            title = yt.title
            audio_stream = yt.streams.filter(only_audio=True).first()
            file_path = audio_stream.download(output_path=DOWNLOAD_FOLDER)
            base, ext = os.path.splitext(file_path)
            new_file = base + ".mp3"
            os.rename(file_path, new_file)

            await message.channel.send(content=f"**{title}**", file=discord.File(new_file))
            os.remove(new_file)

        except Exception as e:
            await message.channel.send(f"Gagal upload lagu: {str(e)}")

import os
bot.run(os.getenv("BOT_TOKEN"))
