import discord
from discord.ext import commands
import os
import requests

TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Config
EMBED_COLOR = discord.Color.blurple()
FOOTER_TEXT = "FreedomGDPS Bot • Powered by Fless"
THUMBNAIL_URL = "https://fless.ps.fhgdps.com/logo.png"

# Ready Event
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot {bot.user} is ready!")

# Welcome Message
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        embed = discord.Embed(
            title="Selamat Datang!",
            description=f"Selamat datang {member.mention} di **{member.guild.name}**!",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else THUMBNAIL_URL)
        embed.set_footer(text=FOOTER_TEXT)
        await channel.send(embed=embed)

# Ping Command
@bot.tree.command(name="ping", description="Cek kecepatan bot")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="Pong!", description=f"Latency: `{latency}ms`", color=EMBED_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    await interaction.response.send_message(embed=embed)

# Bot Info
@bot.tree.command(name="botinfo", description="Informasi bot")
async def botinfo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="FreedomGDPS Assistant",
        description="Bot Assistant untuk server FrGDPS!",
        color=EMBED_COLOR
    )
    embed.add_field(name="Developer", value="Fless", inline=True)
    embed.add_field(name="Framework", value="discord.py", inline=True)
    embed.add_field(name="Hosting", value="Railway", inline=True)
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_footer(text=FOOTER_TEXT)
    await interaction.response.send_message(embed=embed)

# Help Command
@bot.tree.command(name="help", description="Lihat semua perintah bot")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="FreedomGDPS Assistant Help", color=EMBED_COLOR)
    embed.add_field(name="/ping", value="Cek kecepatan bot", inline=False)
    embed.add_field(name="/botinfo", value="Info tentang bot", inline=False)
    embed.add_field(name="/gdpsinfo", value="Level terbaru di FreedomGDPS", inline=False)
    embed.add_field(name="/serverinfo", value="Informasi server Discord", inline=False)
    embed.add_field(name="/userinfo", value="Informasi tentang member", inline=False)
    embed.add_field(name="/kick", value="Kick member", inline=False)
    embed.add_field(name="/ban", value="Ban member", inline=False)
    embed.add_field(name="/unban", value="Unban member", inline=False)
    embed.add_field(name="/clear", value="Hapus pesan dalam jumlah tertentu", inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await interaction.response.send_message(embed=embed)

# GDPS Info
@bot.tree.command(name="gdpsinfo", description="Lihat level terbaru di GDPS")
async def gdpsinfo(interaction: discord.Interaction):
    try:
        response = requests.post("https://fless.ps.fhgdps.com/getGJLevels21.php", data={
            "secret": "Wmfd2893gb7",
            "type": "0",
            "str": "",
            "diff": "-",
            "len": "-",
            "page": "0",
        })
        if response.status_code == 200:
            data = response.text.split("|")
            embed = discord.Embed(
                title="FreedomGDPS - Level Terbaru",
                description="Berikut beberapa level terakhir:",
                color=EMBED_COLOR
            )
            for level in data[:5]:
                info = level.split(":")
                if len(info) > 3:
                    embed.add_field(name=f"{info[3]}", value=f"by {info[6]}", inline=False)
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(text=FOOTER_TEXT)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Gagal mengambil data dari GDPS.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}", ephemeral=True)

# Server Info
@bot.tree.command(name="serverinfo", description="Lihat informasi server Discord")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=guild.name, color=EMBED_COLOR)
    embed.add_field(name="Member Count", value=guild.member_count)
    embed.add_field(name="Server Owner", value=guild.owner)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else THUMBNAIL_URL)
    embed.set_footer(text=FOOTER_TEXT)
    await interaction.response.send_message(embed=embed)

# User Info
@bot.tree.command(name="userinfo", description="Lihat informasi tentang member")
async def userinfo(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=f"User Info - {member}", color=EMBED_COLOR)
    embed.add_field(name="Username", value=member.name)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Status", value=member.status)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else THUMBNAIL_URL)
    embed.set_footer(text=FOOTER_TEXT)
    await interaction.response.send_message(embed=embed)

# Kick Command
@bot.tree.command(name="kick", description="Kick member dari server")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Tidak ada alasan"):
    await member.kick(reason=reason)
    embed = discord.Embed(
        title="Member di-Kick",
        description=f"{member.mention} telah di-kick.\n**Alasan:** {reason}",
        color=EMBED_COLOR
    )
    embed.set_footer(text=FOOTER_TEXT)
    await interaction.response.send_message(embed=embed)

# Ban Command
@bot.tree.command(name="ban", description="Ban member dari server")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Tidak ada alasan"):
    await member.ban(reason=reason)
    embed = discord.Embed(
        title="Member di-Ban",
        description=f"{member.mention} telah di-ban.\n**Alasan:** {reason}",
        color=EMBED_COLOR
    )
    embed.set_footer(text=FOOTER_TEXT)
    await interaction.response.send_message(embed=embed)

# Unban Command
@bot.tree.command(name="unban", description="Unban member dari server")
async def unban(interaction: discord.Interaction, user_id: int):
    user = await bot.fetch_user(user_id)
    await interaction.guild.unban(user)
    embed = discord.Embed(
        title="Member di-Unban",
        description=f"{user.mention} telah di-unban.",
        color=EMBED_COLOR
    )
    embed.set_footer(text=FOOTER_TEXT)
    await interaction.response.send_message(embed=embed)

# Clear Messages
@bot.tree.command(name="clear", description="Hapus sejumlah pesan")
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    embed = discord.Embed(
        title="Pesan Dihapus",
        description=f"{amount} pesan berhasil dihapus!",
        color=EMBED_COLOR
    )
    embed.set_footer(text=FOOTER_TEXT)
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(TOKEN)
