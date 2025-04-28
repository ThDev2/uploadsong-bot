import os
import discord
from discord.ext import commands
from discord import app_commands

# Bot Setup
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class FlessBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=os.environ.get("APPLICATION_ID")  # optional kalau mau
        )

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Slash commands synced! Bot siap.")

bot = FlessBot()

# ===== Event: Bot Ready =====
@bot.event
async def on_ready():
    activity = discord.Game(name="/help | FlessGDBot aktif!")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Bot {bot.user.name} aktif! ✨")

# ===== Slash Commands =====

@bot.tree.command(name="ping", description="Cek koneksi bot.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="Pong!", description=f"Latensi: `{latency}ms`", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="Hapus sejumlah pesan.")
@app_commands.describe(amount="Jumlah pesan yang mau dihapus.")
async def clear(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("Kamu tidak punya izin untuk menghapus pesan.", ephemeral=True)
        return
    deleted = await interaction.channel.purge(limit=amount)
    embed = discord.Embed(
        title="Pesan Dihapus",
        description=f"Berhasil menghapus `{len(deleted)}` pesan!",
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="userinfo", description="Lihat info tentang member.")
@app_commands.describe(member="Member yang ingin dilihat.")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f"Info {member}", color=discord.Color.blurple())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Bergabung", value=member.joined_at.strftime("%d %B %Y"))
    embed.set_thumbnail(url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serverinfo", description="Lihat info server ini.")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.gold())
    embed.add_field(name="Nama Server", value=guild.name, inline=False)
    embed.add_field(name="Jumlah Member", value=guild.member_count)
    embed.add_field(name="Owner", value=str(guild.owner))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="botinfo", description="Informasi tentang bot.")
async def botinfo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="FlessGDBot",
        description="Dibuat penuh cinta oleh Amelia untuk Fless~ (◕‿◕✿)",
        color=discord.Color.purple()
    )
    embed.add_field(name="Website", value="[fless.ps.fhgdps.com](https://fless.ps.fhgdps.com)", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="say", description="Bot mengulang pesanmu.")
@app_commands.describe(message="Apa yang mau dikatakan bot?")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

@bot.tree.command(name="avatar", description="Lihat avatar member.")
@app_commands.describe(member="Member yang ingin dilihat.")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f"Avatar {member}", color=discord.Color.random())
    embed.set_image(url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="createembed", description="Buat custom embed sendiri.")
@app_commands.describe(
    title="Judul embed",
    description="Deskripsi embed",
    color="Warna embed (HEX, contoh: #FF5733)"
)
async def createembed(interaction: discord.Interaction, title: str, description: str, color: str = "#3498db"):
    try:
        if not color.startswith("#"):
            color = f"#{color}"
        color_int = int(color[1:], 16)
        embed = discord.Embed(title=title, description=description, color=color_int)
        await interaction.response.send_message(embed=embed)
    except ValueError:
        await interaction.response.send_message("Format warna salah! Gunakan HEX misal `#FF5733`.", ephemeral=True)

@bot.tree.command(name="help", description="Lihat semua perintah bot ini.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="FlessGDBot Commands", description="Semua fitur keren yang bisa kamu pakai:", color=discord.Color.blue())
    embed.add_field(name="/ping", value="Cek koneksi bot", inline=False)
    embed.add_field(name="/clear", value="Hapus pesan", inline=False)
    embed.add_field(name="/userinfo", value="Lihat info member", inline=False)
    embed.add_field(name="/serverinfo", value="Info server", inline=False)
    embed.add_field(name="/botinfo", value="Info tentang bot", inline=False)
    embed.add_field(name="/say", value="Bot mengulang pesanmu", inline=False)
    embed.add_field(name="/avatar", value="Lihat avatar member", inline=False)
    embed.add_field(name="/createembed", value="Buat embed sendiri", inline=False)
    await interaction.response.send_message(embed=embed)

# ===== Run Bot =====
if __name__ == "__main__":
    if TOKEN is None:
        print("DISCORD_TOKEN tidak ditemukan.")
    else:
        bot.run(TOKEN)
