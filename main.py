import os
import discord
import aiohttp
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
            application_id=os.environ.get("APPLICATION_ID")
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
    embed.add_field(name="Bergabung", value=member.joined_at.strftime("%d %B %Y"))
    embed.set_thumbnail(url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

# Server Info
@bot.tree.command(name="serverinfo", description="Lihat info server ini.")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.gold())
    embed.add_field(name="Nama Server", value=guild.name, inline=False)
    embed.add_field(name="Jumlah Member", value=guild.member_count)
    embed.add_field(name="Owner", value=str(guild.owner))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
    await interaction.response.send_message(embed=embed)

# Bot Info
@bot.tree.command(name="botinfo", description="Informasi tentang bot.")
async def botinfo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="FlessGDBot :billed_cap:",
        description="FlessGDBot adalah bot Discord resmi untuk FreedomGDPS. Di-Support Oleh GiffariRMX Dan DANZGAME. Beta Tester RedBlue Dan Thio",
        color=discord.Color.purple()
    )
    embed.add_field(name="Website Kami", value="[fless.ps.fhgdps.com](https://fless.ps.fhgdps.com)", inline=False)
    await interaction.response.send_message(embed=embed)

# Say
@bot.tree.command(name="gtw", description="Bot mengulang pesanmu.")
@app_commands.describe(message="Apa yang kamu mau bot katakan?")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

# Avatar
@bot.tree.command(name="avatar", description="Lihat avatar member.")
@app_commands.describe(member="Member yang ingin dilihat.")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f"Avatar {member}", color=discord.Color.random())
    embed.set_image(url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

# Create Embed
@bot.tree.command(name="createembed", description="Buat custom embed sendiri.")
@app_commands.describe(
    title="Judul",
    description="isi nya?",
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
        await interaction.response.send_message("Format warna salah sayang! Gunakan HEX misal `#FF5733`.", ephemeral=True)

# Help
@bot.tree.command(name="help", description="Lihat semua perintah bot ini.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="FlessGDBot Commands", description="Semua fitur keren yang bisa kamu pakai:", color=discord.Color.blue())
    embed.add_field(name="/ping", value="Cek koneksi bot", inline=False)
    embed.add_field(name="/clear", value="Hapus pesan", inline=False)
    embed.add_field(name="/userinfo", value="Lihat info member", inline=False)
    embed.add_field(name="/serverinfo", value="Info server", inline=False)
    embed.add_field(name="/botinfo", value="Info tentang bot", inline=False)
    embed.add_field(name="/gtw", value="Bot mengulang pesanmu", inline=False)
    embed.add_field(name="/avatar", value="Lihat avatar member", inline=False)
    embed.add_field(name="/createembed", value="Buat embed sendiri", inline=False)
    embed.add_field(name="/searchsong", value="Cari lagu di database kamu", inline=False)
    embed.add_field(name="/gdpsinfo", value="Info server FrGDPS", inline=False)
    embed.add_field(name="/levelinfo", value="Cari level di FrGDPS", inline=False)
    await interaction.response.send_message(embed=embed)

# Search Song
@bot.tree.command(name="searchsong", description="Cari lagu di database kamu.")
@app_commands.describe(query="Judul lagu yang mau dicari.")
async def searchsong(interaction: discord.Interaction, query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://fless.ps.fhgdps.com/dashboard/api/songs.php?query={query}") as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("success"):
                    embed = discord.Embed(title="Hasil Lagu", color=discord.Color.green())
                    embed.add_field(name="Judul", value=data["name"], inline=False)
                    embed.add_field(name="Author", value=data["author"], inline=False)
                    embed.add_field(name="ID", value=data["id"], inline=False)
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("Lagu tidak ditemukan!", ephemeral=True)
            else:
                await interaction.response.send_message("Gagal mengakses database.", ephemeral=True)

# GDPS Info
@bot.tree.command(name="gdpsinfo", description="Lihat info tentang GDPS.")
async def gdpsinfo(interaction: discord.Interaction):
    embed = discord.Embed(title="FreedomGDPS Info", color=discord.Color.gold())
    embed.add_field(name="Nama Server", value="FreedomGDPS!!11", inline=False)
    embed.add_field(name="Website", value="[Klik Disini](https://fless.ps.fhgdps.com)", inline=False)
    embed.add_field(name="Status", value="Online", inline=False)
    await interaction.response.send_message(embed=embed)

# Level Info
@bot.tree.command(name="levelinfo", description="Cari level di GDPS.")
@app_commands.describe(id="ID level yang mau dicari.")
async def levelinfo(interaction: discord.Interaction, id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://fless.ps.fhgdps.com/dashboard/api/searchLevel.php?id={id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("success"):
                    embed = discord.Embed(title="Level Info", color=discord.Color.blue())
                    embed.add_field(name="Nama Level", value=data["name"], inline=False)
                    embed.add_field(name="Creator", value=data["creator"], inline=False)
                    embed.add_field(name="Difficulty", value=data["difficulty"], inline=False)
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("Level tidak ditemukan!", ephemeral=True)
            else:
                await interaction.response.send_message("Gagal mengakses database.", ephemeral=True)

# ===== Run Bot =====
if __name__ == "__main__":
    if TOKEN is None:
        print("DISCORD_TOKEN tidak ditemukan.")
    else:
        bot.run(TOKEN)
