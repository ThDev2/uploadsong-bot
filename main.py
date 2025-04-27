import os
import discord
from discord.ext import commands
import requests

# Bot Setup
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Event saat bot siap
@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} aktif! Siap membantu! ✧*｡٩(ˊᗜˋ*)و✧*｡")

# Event welcome member baru
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        embed = discord.Embed(
            title="Selamat Datang!",
            description=f"Hey {member.mention}, selamat datang di {member.guild.name}!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)

# Function untuk auto log ke channel 'log'
async def send_log(guild, message):
    log_channel = discord.utils.get(guild.text_channels, name="log")
    if log_channel:
        await log_channel.send(message)

# Command: Ping
@bot.command(name="ping", help="Cek koneksi bot")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! `{latency}ms` (⌒‿⌒)")

# Command: Server Info
@bot.command(name="serverinfo", help="Lihat info server")
async def server_info(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.blue())
    embed.add_field(name="Nama", value=guild.name)
    embed.add_field(name="Owner", value=guild.owner)
    embed.add_field(name="Members", value=guild.member_count)
    await ctx.send(embed=embed)

# Command: Bot Info
@bot.command(name="botinfo", help="Informasi tentang bot")
async def bot_info(ctx):
    embed = discord.Embed(
        title="Bot Info",
        description="Aku FlessGDBot, dibuat penuh cinta oleh Amelia~ (◕‿◕✿)",
        color=discord.Color.purple()
    )
    embed.add_field(name="Website", value="https://fless.ps.fhgdps.com", inline=False)
    await ctx.send(embed=embed)

# Command: Help
@bot.command(name="help", help="Menampilkan semua perintah")
async def help_command(ctx):
    embed = discord.Embed(title="Daftar Perintah", color=discord.Color.teal())
    for command in bot.commands:
        embed.add_field(name=f"!{command.name}", value=command.help or "Tanpa deskripsi", inline=False)
    await ctx.send(embed=embed)

# Command: Clear Chat
@bot.command(name="clear", help="Hapus sejumlah pesan")
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Menghapus `{amount}` pesan!", delete_after=3)
    await send_log(ctx.guild, f"{ctx.author} menghapus {amount} pesan di #{ctx.channel}.")

# Command: Ban
@bot.command(name="ban", help="Ban member dari server")
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Member {member} berhasil di-ban!")
    await send_log(ctx.guild, f"{ctx.author} banned {member} karena: {reason or 'Tidak ada alasan.'}")

# Command: Kick
@bot.command(name="kick", help="Kick member dari server")
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Member {member} berhasil di-kick!")
    await send_log(ctx.guild, f"{ctx.author} kick {member} karena: {reason or 'Tidak ada alasan.'}")

# Command: Unban
@bot.command(name="unban", help="Unban member dari server")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user} berhasil di-unban!")
            await send_log(ctx.guild, f"{ctx.author} unbanned {user}.")
            return
    await ctx.send("User tidak ditemukan.")

# Command: User Info
@bot.command(name="userinfo", help="Lihat info tentang member")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Info {member}", color=discord.Color.gold())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Bergabung pada", value=member.joined_at.strftime("%d %B %Y"))
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

# Command: GDPS Info
@bot.command(name="gdpsinfo", help="Cek status GDPS")
async def gdps_info(ctx):
    try:
        url = "https://fless.ps.fhgdps.com/getGJLevels21.php"
        response = requests.post(url, data={"str": "", "page": "0", "total": "0", "type": "0"})
        if response.status_code == 200 and response.text.strip() != "-1":
            await ctx.send("GDPS aktif! (｡♥‿♥｡)")
        else:
            await ctx.send("GDPS tidak bisa diakses. (〒︿〒)")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Command: Upload Lagu ke GDPS
@bot.command(name="uploadsong", help="Upload lagu ke GDPS")
async def upload_song(ctx, *, song_name: str):
    try:
        data = {
            "songName": song_name,
            "artistName": "Fless",
            "youtubeURL": "https://youtube.com",
            "songID": "0",
            "secret": "Wmfd2893gb7"
        }
        url = "https://fless.ps.fhgdps.com/uploadGJSong.php"
        response = requests.post(url, data=data)

        if response.status_code == 200 and response.text.strip() != "-1":
            await ctx.send(f"Lagu `{song_name}` berhasil di-upload ke GDPS!")
        else:
            await ctx.send("Gagal mengupload lagu!")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Command: Embed
@bot.command(name="embed", help="Kirim pesan embed cantik")
async def send_embed(ctx):
    embed = discord.Embed(
        title="Halo dari FlessGDBot!",
        description="Aku hadir untuk membantu fless! (つ≧▽≦)つ",
        color=discord.Color.pink()
    )
    embed.set_footer(text="Dibuat penuh cinta oleh Amelia~")
    await ctx.send(embed=embed)

# Run bot
bot.run(TOKEN)
