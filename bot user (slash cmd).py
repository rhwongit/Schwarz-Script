import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import asyncio
import random

# Enter Bot's Token
TOKEN = 'BOT_TOKEN'

# Set up the bot with a command prefix (default prefix '?')
intents = discord.Intents.default()
intents.message_content = True  # Enable the bot to read message content
intents.members = True  # Needed for member commands
bot = commands.Bot(command_prefix="?", intents=intents)

# Log channel ID
LOG_CHANNEL_ID = 1233364665 # Replace it with your Channel ID
# Dictionary to track conversation state
joke_state = {}

# Dictionary to store jokes
jokes = {
    1: {
        "setup": "YOUR JOKE",
        "punchline": "YOUR PUNCHLINE:"
    },
    2: {
        "setup": "YOUR JOKE",
        "punchline": "YOUR PUNCHLINE"
    }
} # Add More If Needed

@bot.event
async def on_ready():
    print(f'Bot has started {bot.user.name} (ID: {bot.user.id})')
    print('------')
    
    # Sync slash commands to specific guild for instant updates
    GUILD_ID = 12312311456  # Replace with your server ID
    guild = discord.Object(id=GUILD_ID)
    
    try:
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print(f"Slash commands synced to guild {GUILD_ID}")
    except Exception as e:
        print(f"Error syncing slash commands: {e}")

# =====================
# HYBRID COMMANDS (WORK WITH BOTH ? AND /)
# =====================

@bot.hybrid_command(name="ping", description="Check bot's latency")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"da latency is: **{latency}ms**\nAm i fast enough to waste your fucking time?")

@bot.hybrid_command(name="ban", description="Ban a user from the server")
@app_commands.describe(member="Member to ban", reason="Reason for ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned :hammer: {member.mention} Reason: {reason}")
    await send_log(ctx, "Ban", member, reason)

@bot.hybrid_command(name="kick", description="Kick a user from the server")
@app_commands.describe(member="Member to kick", reason="Reason for kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention} Reason: {reason}")
    await send_log(ctx, "Kick", member, reason)

@bot.hybrid_command(name="mute", description="Mute a user for duration")
@app_commands.describe(
    member="Member to mute",
    duration="Duration number",
    unit="Time unit (minutes/hours/days)",
    reason="Reason for mute"
)
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: int, unit: str = "minutes", *, reason: str = None):
    try:
        unit = unit.lower()
        if unit in ["min", "minutes"]:
            duration_seconds = duration * 60
            display_duration = f"{duration} minute(s)"
        elif unit in ["hour", "hours"]:
            duration_seconds = duration * 3600
            display_duration = f"{duration} hour(s)"
        elif unit in ["day", "days"]:
            duration_seconds = duration * 86400
            display_duration = f"{duration} day(s)"
        else:
            await ctx.send("Invalid unit. Use: minutes, hours, or days")
            return

        muted_role = get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(muted_role, send_messages=False, add_reactions=False)

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"Muted {member.mention} for {display_duration}. Reason: {reason}")
        await send_log(ctx, "Mute", member, reason, display_duration)

        await asyncio.sleep(duration_seconds)
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"Unmuted {member.mention} after {display_duration}.")

    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.hybrid_command(name="unmute", description="Unmute a user")
@app_commands.describe(member="Member to unmute")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    muted_role = get(ctx.guild.roles, name="Muted")
    if muted_role and muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f"Unmuted {member.mention}")
        await send_log(ctx, "Unmute", member)
    else:
        await ctx.send(f"{member.mention} is not muted.")

@bot.hybrid_command(name="warn", description="Warn a user")
@app_commands.describe(member="Member to warn", reason="Reason for warning")
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason: str):
    await ctx.send(f"Warned :warning: {member.mention} Reason: {reason}")
    await send_log(ctx, "Warn", member, reason)

@bot.hybrid_command(name="clear", description="Clear messages")
@app_commands.describe(amount="Number of messages to delete")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    if amount <= 0:
        await ctx.send("Number must be positive!", ephemeral=True)
        return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Cleared {amount} fucking messages", delete_after=3)

# =====================
# SLASH COMMAND ONLY
# =====================

@bot.tree.command(name="joke", description="Tell a random joke")
async def joke(interaction: discord.Interaction):
    joke_id = random.choice(list(jokes.keys()))
    await interaction.response.send_message(jokes[joke_id]["setup"])
    joke_state[interaction.user.id] = joke_id

# =====================
# MESSAGE HANDLING
# =====================

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    
    if content == "MESSAGE":
        await message.reply("RESPONSE", mention_author=False)
    elif content == "MESSAGE":
        await message.reply("RESPONSE", mention_author=False)
    elif content == "MESSAGE":
        await message.reply("RESPONSE", mention_author=False)
    elif content == "MESSAGE":
        await message.reply("RESPONSE", mention_author=False)
    elif content == "MESSAGE":
        await message.reply("RESPONSE")
    elif content == "MESSAGE":
        await message.reply("RESPONSE") # Add More If Needed
    elif content == "tell me a joke":
        joke_id = random.choice(list(jokes.keys()))
        await message.channel.send(jokes[joke_id]["setup"])
        joke_state[message.author.id] = joke_id
    elif content in ["why", "why?"] and joke_state.get(message.author.id):
        joke_id = joke_state[message.author.id]
        await message.channel.send(jokes[joke_id]["punchline"])
        joke_state[message.author.id] = None

    await bot.process_commands(message)

# =====================
# LOGGING SYSTEM
# =====================

async def send_log(ctx, action: str, member: discord.Member, reason: str = None, duration: str = None):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        return

    embed = discord.Embed(
        title=f"Action: {action}",
        color=discord.Color.red() if action in ["Ban", "Kick", "Mute"] else discord.Color.green()
    )
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Moderator", value=ctx.author.mention)
    if reason: embed.add_field(name="Reason", value=f"```{reason}```" if reason else "No reason provided")
    if duration: embed.add_field(name="Duration", value=duration)

    try:
        await log_channel.send(embed=embed)
    except:
        log_message = f"**Action:** {action}\n**User:** {member.mention}\n**Moderator:** {ctx.author.mention}"
        if reason: log_message += f"\n**Reason:** {reason}"
        if duration: log_message += f"\n**Duration:** {duration}"
        await log_channel.send(log_message)

# =====================
# ERROR HANDLING
# =====================

@ban.error
@kick.error
@mute.error
@unmute.error
@warn.error
async def mod_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission for this command!", ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument!", ephemeral=True)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument!", ephemeral=True)
    else:
        await ctx.send(f"Error: {error}", ephemeral=True)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Specify number of messages to clear", ephemeral=True)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid number", ephemeral=True)

# Run the bot
bot.run(TOKEN)
