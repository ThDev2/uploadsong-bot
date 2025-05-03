import os
import discord
import requests
from discord.ext import commands
from discord import app_commands

# Bot Setup
TOKEN = os.environ.get("DISCORD_TOKEN")
API_BASE = "https://fless.ps.fhgdps.com/dashboard/api/"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class FlessBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=os.environ.get("APPLICATION_ID")
        )

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Slash commands synced! Bot siap.")

bot = FlessBot()

@bot.event
async def on_ready():
    activity = discord.Game(name="/help | FlessGDBot aktif!")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Bot {bot.user.name} aktif!")

# Ping
@bot.tree.command(name="ping", description="Cek koneksi bot.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="Pong!", description=f"Latensi: `{latency}ms`", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

# Clear
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

# User Info
@bot.tree.command(name="userinfo", description="Lihat info tentang member.")
@app_commands.describe(member="Member yang ingin dilihat.")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f"Info {member}", color=discord.Color.blurple())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Bergabung", value=member.joined_at.strftime("%d %B %Y") if member.joined_at else "Tidak diketahui")
    embed.set_thumbnail(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# Server Info
@bot.tree.command(name="serverinfo", description="Lihat info server ini.")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.gold())
    embed.add_field(name="Nama Server", value=guild.name, inline=False)
    embed.add_field(name="Jumlah Member", value=guild.member_count)
    embed.add_field(name="Owner", value=str(guild.owner))
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await interaction.response.send_message(embed=embed)

# Bot Info
@bot.tree.command(name="botinfo", description="Informasi tentang bot.")
async def botinfo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="FlessGDBot",
        description="Bot resmi FreedomGDPS. Support: GiffariRMX, DANZGAME. Beta: RedBlue & Thio.",
        color=discord.Color.purple()
    )
    embed.add_field(name="Website Kami", value="[fless.ps.fhgdps.com](https://fless.ps.fhgdps.com)", inline=False)
    await interaction.response.send_message(embed=embed)

# Say
@bot.tree.command(name="gtw", description="Bot mengulang pesanmu.")
@app_commands.describe(message="Apa yang kamu mau bot katakan?")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    await interaction.followup.send(message)

# Avatar
@bot.tree.command(name="avatar", description="Lihat avatar member.")
@app_commands.describe(member="Member yang ingin dilihat.")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f"Avatar {member}", color=discord.Color.random())
    embed.set_image(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# Create Embed
@bot.tree.command(name="createembed", description="Buat custom embed sendiri.")
@app_commands.describe(title="Judul", description="Isi embed", color="Warna HEX, contoh: #FF5733")
async def createembed(interaction: discord.Interaction, title: str, description: str, color: str = "#3498db"):
    await interaction.response.defer()
    try:
        if not color.startswith("#"):
            color = f"#{color}"
        color_int = int(color[1:], 16)
        embed = discord.Embed(title=title, description=description, color=color_int)
        await interaction.followup.send(embed=embed)
    except ValueError:
        await interaction.followup.send("Format warna salah! Gunakan HEX misal `#FF5733`.", ephemeral=True)

# Help
@bot.tree.command(name="help", description="Lihat semua perintah bot ini.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="FlessGDBot Commands", description="Semua fitur keren:", color=discord.Color.blue())
    commands_list = [
        "/ping", "/clear", "/userinfo", "/serverinfo", "/botinfo",
        "/gtw", "/avatar", "/createembed", "/searchsong", "/gdpsinfo",
        "/searchlevel", "/uploadsong", "/stats", "/login", "/profile"
    ]
    for cmd in commands_list:
        embed.add_field(name=cmd, value="\u200b", inline=True)
    await interaction.response.send_message(embed=embed)

# Upload Song
@bot.tree.command(name="uploadsong", description="Upload lagu ke server FrGDPS.")
@app_commands.describe(name="Nama lagu", id="ID lagu", size="Ukuran byte", author="Nama author", download="1/0 bisa diunduh")
async def uploadsong(interaction: discord.Interaction, name: str, id: int, size: int, author: str, download: int):
    await interaction.response.defer()
    try:
        res = requests.post(API_BASE + "addSong.php", data={
            "songName": name, "songID": id, "songSize": size, "songAuthor": author, "download": download
        })
        await interaction.followup.send(f"Response: {res.text}")
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

# Search Level
@bot.tree.command(name="searchlevel", description="Cari level berdasarkan nama.")
@app_commands.describe(query="Nama level")
async def searchlevel(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    try:
        res = requests.post(API_BASE + "searchLevel.php", data={"query": query})
        await interaction.followup.send(f"Result: {res.text}")
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

# Who Rated
@bot.tree.command(name="whorated", description="Siapa yang rate level.")
@app_commands.describe(level_id="ID level")
async def whorated(interaction: discord.Interaction, level_id: int):
    await interaction.response.defer()
    try:
        res = requests.post(API_BASE + "whoRated.php", data={"levelID": level_id})
        await interaction.followup.send(f"Rated by: {res.text}")
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

# Stats
@bot.tree.command(name="stats", description="Lihat statistik FrGDPS")
async def stats(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        res = requests.get(API_BASE + "stats.php")
        await interaction.followup.send(f"Stats: {res.text}")
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

# Profile
@bot.tree.command(name="profile", description="Lihat profil user.")
@app_commands.describe(username="Username FrGDPS")
async def profile(interaction: discord.Interaction, username: str):
    await interaction.response.defer()
    try:
        res = requests.post(API_BASE + "profile.php", data={"username": username})
        await interaction.followup.send(f"Profile: {res.text}")
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

# Login
@bot.tree.command(name="login", description="Login user FrGDPS")
@app_commands.describe(username="Username", password="Password")
async def login(interaction: discord.Interaction, username: str, password: str):
    await interaction.response.defer(ephemeral=True)
    try:
        res = requests.post(API_BASE + "login.php", data={"username": username, "password": password})
        await interaction.followup.send(f"Login Response: {res.text}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}", ephemeral=True)

if __name__ == "__main__":
    if TOKEN is None:
        print("DISCORD_TOKEN tidak ditemukan.")
    else:
        bot.run(TOKEN)
