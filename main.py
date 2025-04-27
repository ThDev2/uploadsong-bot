import os
import discord
from discord.ext import commands
from discord import app_commands
import requests

# Bot Setup
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== Event: Bot Ready =====

@bot.event
async def on_ready():
    activity = discord.Game(name="/uploadsong | FlessGDBot aktif!")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Bot {bot.user.name} aktif! ✧*｡٩(ˊᗜˋ*)و✧*｡")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)!")
    except Exception as e:
        print(f"Gagal sync slash commands: {e}")

# ===== Event: Member Join =====

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

# ===== Helper: Send Log to #log =====

async def send_log(guild, message):
    log_channel = discord.utils.get(guild.text_channels, name="log")
    if log_channel:
        await log_channel.send(message)

# ===== Prefix Commands =====

@bot.command(name="ping", help="Cek koneksi bot")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! `{latency}ms` (⌒‿⌒)")

@bot.command(name="serverinfo", help="Lihat info server")
async def server_info(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.blue())
    embed.add_field(name="Nama", value=guild.name)
    embed.add_field(name="Owner", value=guild.owner)
    embed.add_field(name="Members", value=guild.member_count)
    await ctx.send(embed=embed)

@bot.command(name="botinfo", help="Informasi tentang bot")
async def bot_info(ctx):
    embed = discord.Embed(
        title="Bot Info",
        description="Aku FlessGDBot, dibuat penuh cinta oleh Amelia~ (◕‿◕✿)",
        color=discord.Color.purple()
    )
    embed.add_field(name="Website", value="https://fless.ps.fhgdps.com", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="clear", help="Hapus sejumlah pesan")
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Menghapus `{amount}` pesan!", delete_after=3)
    await send_log(ctx.guild, f"{ctx.author} menghapus {amount} pesan di #{ctx.channel}.")

@bot.command(name="ban", help="Ban member dari server")
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Member {member} berhasil di-ban!")
    await send_log(ctx.guild, f"{ctx.author} banned {member} karena: {reason or 'Tidak ada alasan.'}")

@bot.command(name="kick", help="Kick member dari server")
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Member {member} berhasil di-kick!")
    await send_log(ctx.guild, f"{ctx.author} kick {member} karena: {reason or 'Tidak ada alasan.'}")

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

@bot.command(name="userinfo", help="Lihat info tentang member")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Info {member}", color=discord.Color.gold())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Bergabung pada", value=member.joined_at.strftime("%d %B %Y"))
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

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

@bot.command(name="embed", help="Kirim pesan embed cantik")
async def send_embed(ctx):
    embed = discord.Embed(
        title="Halo dari FlessGDBot!",
        description="Aku hadir untuk membantu fless! (つ≧▽≦)つ",
        color=discord.Color.pink()
    )
    embed.set_footer(text="Dibuat penuh cinta oleh Amelia~")
    await ctx.send(embed=embed)

# ===== Slash Commands =====

@bot.tree.command(name="ping", description="Cek apakah bot aktif!")
async def slash_ping(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Pong!",
        description="Bot aktif dan responsif.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="uploadsong", description="Upload lagu ke GDPS kamu!")
@app_commands.describe(song_name="Masukkan nama lagu yang ingin diupload")
async def slash_uploadsong(interaction: discord.Interaction, song_name: str):
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
            embed = discord.Embed(
                title="Upload Lagu Berhasil!",
                description=f"Lagu **{song_name}** berhasil diupload ke GDPS!",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Gagal mengupload lagu!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}", ephemeral=True)

# ===== Error Handler =====

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Sepertinya ada yang kurang... Tolong isi semua parameter dengan benar.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Perintah tidak ditemukan. Coba cek kembali namanya.")
    else:
        await ctx.send(f"Terjadi error: {str(error)}")
        print(f"Error terjadi: {str(error)}")

# ===== Start Bot =====

if __name__ == "__main__":
    if TOKEN is None:
        print("DISCORD_TOKEN tidak ditemukan di environment variables.")
    else:
        bot.run(TOKEN)
