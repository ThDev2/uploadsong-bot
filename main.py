import os
import discord
from discord.ext import commands
from discord import app_commands

# Bot Setup
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== Event: Bot Ready =====

@bot.event
async def on_ready():
    activity = discord.Game(name="/createembed | FlessGDBot aktif!")
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
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Menghapus `{len(deleted) - 1}` pesan!", delete_after=3)
        await send_log(ctx.guild, f"{ctx.author} menghapus {len(deleted) - 1} pesan di #{ctx.channel}.")
    except Exception as e:
        print(f"Error saat clear: {e}")

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

@bot.tree.command(name="createembed", description="Buat custom embed!")
@app_commands.describe(
    title="Judul embed",
    description="Deskripsi embed",
    color="Warna embed dalam format HEX (#RRGGBB)"
)
async def create_embed(interaction: discord.Interaction, title: str, description: str, color: str = "#3498db"):
    try:
        if not color.startswith("#"):
            color = f"#{color}"
        color_int = int(color[1:], 16)
        embed = discord.Embed(
            title=title,
            description=description,
            color=color_int
        )
        await interaction.response.send_message(embed=embed)
    except ValueError:
        await interaction.response.send_message("Format warna salah! Gunakan format HEX, contoh: `#FF5733`.", ephemeral=True)

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
