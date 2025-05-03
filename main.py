import os
import discord
import aiohttp
import requests
from discord.ext import commands

# Bot Setup
TOKEN = os.environ.get("DISCORD_TOKEN")
API_BASE = "https://fless.ps.fhgdps.com/dashboard/api/"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="F ", intents=intents)

# ===== Event: Bot Ready =====
@bot.event
async def on_ready():
    activity = discord.Game(name="F help | FlessGDBot aktif!")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Bot {bot.user.name} aktif! ✨")

# ===== Commands =====

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="Pong!", description=f"Latensi: `{latency}ms`", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(name="clear")
async def clear(ctx, amount: int):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("Kamu tidak punya izin untuk menghapus pesan.")
        return
    deleted = await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title="Pesan Dihapus", description=f"Berhasil menghapus `{len(deleted)}` pesan!", color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Info {member}", color=discord.Color.blurple())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Bergabung", value=member.joined_at.strftime("%d %B %Y"))
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="serverinfo")
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.gold())
    embed.add_field(name="Nama Server", value=guild.name, inline=False)
    embed.add_field(name="Jumlah Member", value=guild.member_count)
    embed.add_field(name="Owner", value=str(guild.owner))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
    await ctx.send(embed=embed)

@bot.command(name="botinfo")
async def botinfo(ctx):
    embed = discord.Embed(
        title="FlessGDBot :billed_cap:",
        description="Bot Discord resmi untuk FreedomGDPS. Di-Support Oleh GiffariRMX Dan DANZGAME. Beta Tester RedBlue Dan Thio",
        color=discord.Color.purple()
    )
    embed.add_field(name="Website Kami", value="[fless.ps.fhgdps.com](https://fless.ps.fhgdps.com)", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="gtw")
async def say(ctx, *, message: str):
    await ctx.send(message)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Avatar {member}", color=discord.Color.random())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="createembed")
async def create_embed(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Masukkan **Judul** dan **Isi** dengan format:\n`Judul: ...`\n`Isi: ...`")

    try:
        msg = await bot.wait_for("message", timeout=180.0, check=check)
        lines = msg.content.split("Isi:")
        if len(lines) < 2:
            return await ctx.send("Format salah. Harus ada `Judul:` dan `Isi:`.")
        
        title_line = lines[0].replace("Judul:", "").strip()
        content = lines[1].strip()

        embed = discord.Embed(description=content, color=0xc2c2c2)
        embed.title = title_line
        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("Waktu habis. Silakan coba lagi.")

@bot.command(name="menu")
async def help_command(ctx):
    embed = discord.Embed(title="FlessGDBot Commands", description="Semua fitur keren yang bisa kamu pakai:", color=discord.Color.blue())
    embed.add_field(name="F ping", value="Cek koneksi bot", inline=False)
    embed.add_field(name="F clear [jumlah]", value="Hapus pesan", inline=False)
    embed.add_field(name="F userinfo", value="Lihat info member", inline=False)
    embed.add_field(name="F serverinfo", value="Info server", inline=False)
    embed.add_field(name="F botinfo", value="Info tentang bot", inline=False)
    embed.add_field(name="F gtw [pesan]", value="Bot mengulang pesanmu", inline=False)
    embed.add_field(name="F avatar", value="Lihat avatar member", inline=False)
    embed.add_field(name="F createembed", value="Buat embed sendiri", inline=False)
    embed.add_field(name="F searchlevel", value="Cari level di FrGDPS", inline=False)
    embed.add_field(name="F uploadsong", value="Upload Lagu di FrGDPS", inline=False)
    embed.add_field(name="F stats", value="Liat Statistik User FrGDPS", inline=False)
    embed.add_field(name="F profile", value="Lihat profil user FrGDPS", inline=False)
    embed.add_field(name="F login", value="Login Akun FrGDPS", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="uploadsong")
async def uploadsong(ctx, name: str, id: int, size: int, author: str, download: int):
    data = {
        "songName": name,
        "songID": id,
        "songSize": size,
        "songAuthor": author,
        "download": download
    }
    try:
        res = requests.post(API_BASE + "addSong.php", data=data)
        await ctx.send(f"Response: {res.text}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="searchlevel")
async def searchlevel(ctx, *, query: str):
    try:
        res = requests.post(API_BASE + "searchLevel.php", data={"query": query})
        await ctx.send(f"Hasil: {res.text}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="whorated")
async def whorated(ctx, level_id: int):
    try:
        res = requests.post(API_BASE + "whoRated.php", data={"levelID": level_id})
        await ctx.send(f"Rated by: {res.text}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="stats")
async def stats(ctx):
    try:
        res = requests.get(API_BASE + "stats.php")
        await ctx.send(f"Stats: {res.text}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="profile")
async def profile(ctx, username: str):
    try:
        res = requests.post(API_BASE + "profile.php", data={"username": username})
        await ctx.send(f"Profile: {res.text}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="login")
async def login(ctx, username: str, password: str):
    try:
        res = requests.post(API_BASE + "login.php", data={"username": username, "password": password})
        await ctx.send(f"Login Response: {res.text}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Jalankan Bot
if __name__ == "__main__":
    if TOKEN is None:
        print("DISCORD_TOKEN tidak ditemukan.")
    else:
        bot.run(TOKEN)
