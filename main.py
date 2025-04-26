import discord
from discord.ext import commands
from discord import app_commands

TOKEN = "ISI_TOKEN_BOT_KAMU"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot {bot.user} sudah aktif.")

@bot.tree.command(name="embed", description="Kirim embed ke channel.")
@app_commands.describe(
    title="Judul embed",
    desc="Isi deskripsi embed",
    color_hex="Warna embed (hex, opsional, contoh: FF0000)"
)
async def embed(
    interaction: discord.Interaction,
    title: str,
    desc: str,
    color_hex: str = "2F3136"
):
    try:
        color = discord.Color(int(color_hex, 16))
        emb = discord.Embed(title=title, description=desc, color=color)
        emb.set_footer(text=f"Embed oleh {interaction.user.name}")
        await interaction.response.send_message(embed=emb)
    except:
        await interaction.response.send_message("Format warna salah. Gunakan hex tanpa # (contoh: FF0000)", ephemeral=True)

bot.run(TOKEN)