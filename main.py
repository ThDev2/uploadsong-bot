import discord
from discord.ext import commands
from discord import app_commands
import os

TOKEN = os.environ["DISCORD_TOKEN"]
LOG_CHANNEL_ID = 0  # Ganti ke ID channel log atau biarkan 0 kalau nggak dipakai

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot {bot.user} aktif dan siap!")

@bot.tree.command(name="embed", description="Kirim embed keren")
@app_commands.describe(
    title="Judul embed",
    desc="Isi deskripsi",
    channel="Channel tujuan",
    role="Mention role (opsional)",
    color_hex="Warna hex (contoh: FF0000)",
    image_url="URL gambar (opsional)",
    thumbnail_url="URL thumbnail (opsional)",
    delete_after="Auto delete (detik, opsional)",
)
async def embed(
    interaction: discord.Interaction,
    title: str,
    desc: str,
    channel: discord.TextChannel,
    role: discord.Role = None,
    color_hex: str = "2F3136",
    image_url: str = "",
    thumbnail_url: str = "",
    delete_after: int = 0
):
    try:
        color = discord.Color(int(color_hex, 16))
    except:
        await interaction.response.send_message("Hex warna salah. Contoh: `FF0000`", ephemeral=True)
        return

    emb = discord.Embed(title=title, description=desc, color=color)
    emb.set_footer(text=f"By {interaction.user.name}")
    emb.timestamp = interaction.created_at

    if image_url:
        emb.set_image(url=image_url)
    if thumbnail_url:
        emb.set_thumbnail(url=thumbnail_url)

    mention = role.mention if role else ""
    msg = await channel.send(content=mention, embed=emb)

    if delete_after > 0:
        await msg.delete(delay=delete_after)

    await interaction.response.send_message(f"Embed dikirim ke {channel.mention}", ephemeral=True)

    if LOG_CHANNEL_ID:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"[LOG] Embed oleh {interaction.user.name} ke {channel.mention}")

bot.run(TOKEN)
