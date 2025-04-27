import os
import discord
from discord.ext import commands
from discord import app_commands
import requests

# ===== Bot Setup =====
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== Event: Bot Ready =====
@bot.event
async def on_ready():
    activity = discord.Game(name="/help | FlessGDBot aktif!")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await bot.tree.sync()
    print(f"Bot {bot.user.name} aktif!")

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

# ===== Helper =====
async def send_log(guild, message):
    log_channel = discord.utils.get(guild.text_channels, name="log")
    if log_channel:
        await log_channel.send(message)

# ===== Slash Commands =====

@bot.tree.command(name="ping", description="Cek koneksi bot")
async def slash_ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="Pong!",
        description=f"Bot responsif! `{latency}ms`",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serverinfo", description="Lihat info server")
async def slash_serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.blue())
    embed.add_field(name="Nama", value=guild.name)
    embed.add_field(name="Owner", value=guild.owner)
    embed.add_field(name="Members", value=guild.member_count)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="botinfo", description="Informasi tentang bot ini")
async def slash_botinfo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Tentang FlessGDBot",
        description="Aku FlessGDBot, dibuat penuh cinta oleh Amelia~",
        color=discord.Color.purple()
    )
    embed.add_field(name="Website", value="https://fless.ps.fhgdps.com", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="Hapus sejumlah pesan di channel")
@app_commands.describe(amount="Jumlah pesan yang mau dihapus")
async def slash_clear(interaction: discord.Interaction, amount: int = 5):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"Menghapus `{amount}` pesan!", ephemeral=True)
    await send_log(interaction.guild, f"{interaction.user} menghapus {amount} pesan di #{interaction.channel}.")

@bot.tree.command(name="ban", description="Ban member dari server")
@app_commands.describe(member="Member yang ingin di-ban", reason="Alasan ban")
async def slash_ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Tidak ada alasan."):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member.mention} telah di-ban!")
    await send_log(interaction.guild, f"{interaction.user} banned {member} karena: {reason}")

@bot.tree.command(name="kick", description="Kick member dari server")
@app_commands.describe(member="Member yang ingin di-kick", reason="Alasan kick")
async def slash_kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Tidak ada alasan."):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.mention} telah di-kick!")
    await send_log(interaction.guild, f"{interaction.user} kick {member} karena: {reason}")

@bot.tree.command(name="unban", description="Unban member dari server")
@app_commands.describe(member="Contoh format: Nama#1234")
async def slash_unban(interaction: discord.Interaction, member: str):
    banned_users = await interaction.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"{user.mention} telah di-unban!")
            await send_log(interaction.guild, f"{interaction.user} unbanned {user}.")
            return
    await interaction.response.send_message("User tidak ditemukan.", ephemeral=True)

@bot.tree.command(name="userinfo", description="Lihat info tentang member")
@app_commands.describe(member="Member yang mau dilihat (opsional)")
async def slash_userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f"Info {member}", color=discord.Color.gold())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Bergabung pada", value=member.joined_at.strftime("%d %B %Y"))
    embed.set_thumbnail(url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="gdpsinfo", description="Cek status server GDPS")
async def slash_gdpsinfo(interaction: discord.Interaction):
    try:
        url = "https://fless.ps.fhgdps.com/getGJLevels21.php"
        response = requests.post(url, data={"str": "", "page": "0", "total": "0", "type": "0"})
        if response.status_code == 200 and response.text.strip() != "-1":
            await interaction.response.send_message("GDPS aktif! (｡♥‿♥｡)")
        else:
            await interaction.response.send_message("GDPS tidak bisa diakses. (〒︿〒)")
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")

@bot.tree.command(name="embed", description="Kirim embed cantik")
async def slash_embed(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Halo dari FlessGDBot!",
        description="Aku hadir untuk membantu fless! (つ≧▽≦)つ",
        color=discord.Color.pink()
    )
    embed.set_footer(text="Dibuat penuh cinta oleh Amelia~")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="uploadsong", description="Upload lagu ke GDPS!")
@app_commands.describe(song_name="Nama lagu yang ingin diupload")
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
            await interaction.response.send_message("Gagal mengupload lagu.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}", ephemeral=True)

@bot.tree.command(name="help", description="Lihat semua perintah")
async def slash_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Daftar Perintah",
        description="Semua perintah slash yang tersedia di FlessGDBot:",
        color=discord.Color.teal()
    )
    commands_list = [
        "/ping - Cek koneksi bot",
        "/serverinfo - Info server",
        "/botinfo - Info tentang bot",
        "/clear - Hapus pesan",
        "/ban - Ban member",
        "/kick - Kick member",
        "/unban - Unban member",
        "/userinfo - Info member",
        "/gdpsinfo - Cek status GDPS",
        "/embed - Kirim embed",
        "/uploadsong - Upload lagu ke GDPS"
    ]
    embed.add_field(name="Commands", value="\n".join(commands_list), inline=False)
    await interaction.response.send_message(embed=embed)

# ===== Start Bot =====
if __name__ == "__main__":
    if TOKEN is None:
        print("DISCORD_TOKEN tidak ditemukan di environment variables.")
    else:
        bot.run(TOKEN)
