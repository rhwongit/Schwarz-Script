import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import asyncio
import random

# Bot setup
TOKEN = 'BOT_TOKEN'

LOG_CHANNEL_ID = 123456789 # Replace with your log channel ID

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="?", intents=intents)

# Joke system
joke_state = {}
jokes = {
    1: {
        "setup": "YOUR JOKE",
        "punchline": "YOUR PUNCHLINE:"
    },
    2: {
        "setup": "YOUR JOKE",
        "punchline": "YOUR PUNCHLINE"
    }
} #Add More Jokes If Needed

@bot.event
async def on_ready():
    print(f'Bot has started {bot.user.name}')
    
    # Fast sync to specific guild
    GUILD_ID = 123124566889  # Your server ID
    guild = discord.Object(id=GUILD_ID)
    
    try:
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print(f"Slash commands synced to guild {GUILD_ID}")
    except Exception as e:
        print(f"Sync error: {e}")

# =====================
# ALL SLASH COMMANDS
# =====================

@bot.hybrid_command(name="ping", description="Check bot latency")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Latency: **{latency}ms**")

@bot.hybrid_command(name="ban", description="Ban a member")
@app_commands.describe(member="Member to ban", reason="Reason for ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")
    await send_log(ctx, "Ban", member, reason)

@bot.hybrid_command(name="kick", description="Kick a member")
@app_commands.describe(member="Member to kick", reason="Reason for kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")
    await send_log(ctx, "Kick", member, reason)

@bot.hybrid_command(name="mute", description="Mute a member")
@app_commands.describe(
    member="Member to mute",
    duration="Duration number",
    unit="minutes/hours/days",
    reason="Reason for mute"
)
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: int, unit: str = "minutes", *, reason: str = None):
    # ... (keep your existing mute logic)
    await ctx.send(f"Muted {member.mention}")

@bot.hybrid_command(name="unmute", description="Unmute a member")
@app_commands.describe(member="Member to unmute")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    muted_role = get(ctx.guild.roles, name="Muted")
    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f"Unmuted {member.mention}")
    else:
        await ctx.send("User isn't muted!")

@bot.hybrid_command(name="clear", description="Clear messages")
@app_commands.describe(amount="Number of messages to delete")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Cleared {amount} messages", delete_after=3)

@bot.hybrid_command(name="warn", description="Warn a member")
@app_commands.describe(member="Member to warn", reason="Reason for warning")
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason: str):
    await ctx.send(f"Warned {member.mention}")
    await send_log(ctx, "Warn", member, reason)

@bot.hybrid_command(name="joke", description="Tell a random joke")
async def joke(ctx):
    joke_id = random.choice(list(jokes.keys()))
    await ctx.send(jokes[joke_id]["setup"])
    joke_state[ctx.author.id] = joke_id

# =====================
# MESSAGE COMMANDS
# =====================

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    
    if content == "lmao":
        await message.reply("lmao up yo ass")
    elif content in ["why", "why?"] and joke_state.get(message.author.id):
        joke_id = joke_state[message.author.id]
        await message.channel.send(jokes[joke_id]["punchline"])
        joke_state[message.author.id] = None

    await bot.process_commands(message)

# =====================
# UTILITY FUNCTIONS
# =====================

async def send_log(ctx, action: str, member: discord.Member, reason: str = None, duration: str = None):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(title=f"Action: {action}", color=0xff0000)
        embed.add_field(name="User", value=member.mention)
        embed.add_field(name="Moderator", value=ctx.author.mention)
        if reason: embed.add_field(name="Reason", value=reason)
        if duration: embed.add_field(name="Duration", value=duration)
        await log_channel.send(embed=embed)

# Error handling
@ban.error
@kick.error
@mute.error
async def mod_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Missing permissions!", ephemeral=True)

bot.run(TOKEN)
