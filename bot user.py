import discord
from discord.ext import commands
from discord.utils import get
import asyncio  # Import asyncio for the timer

# Enter Bot's Token
TOKEN = 'YOUR BOT TOKEN'

# Set up the bot with a command prefix (default prefix '?')
intents = discord.Intents.default()
intents.message_content = True  # Enable the bot to read message content
bot = commands.Bot(command_prefix="?", intents=intents)

# Log channel ID
LOG_CHANNEL_ID = "1234567890123456789" # Replace this with your log channel ID

# Dictionary to track conversation state
joke_state = {}

# Dictionary to store jokes (setup and punchline)
jokes = {
    1: {
        "setup": "PLACE YOUR JOKE HERE",
        "punchline": "PLACE YOUR JOKE'S PUNCHLINE"
    },
    2: {
        "setup": "PLACE YOUR JOKE HERE",
        "punchline": "PLACE YOUR JOKE'S PUNCHLINE"
    }
} # Add more jokes if needed

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')
    
# Event: When a message is sent
@bot.event
async def on_message(message):
    global joke_state

    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Convert the message content to lowercase for case-insensitive matching
    content = message.content.lower()

    # Respond to specific messages
    if content == "PLACE MESSAGE HERE":
        await message.reply("PLACE YOUR RESPONSE HERE", mention_author=False)
    elif content == "PLACE MESSAGE HERE":
        await message.reply("PLACE YOUR RESPONSE HERE", mention_author=False)
    elif content == "PLACE MESSAGE HERE":
        await message.reply("PLACE YOUR RESPONSE HERE", mention_author=False)
    elif content == "PLACE MESSAGE HERE":
        await message.reply("PLACE YOUR RESPONSE HERE", mention_author=False)
    elif content == "PLACE MESSAGE HERE":
        await message.reply("PLACE YOUR RESPONSE HERE")
    elif content == "PLACE MESSAGE HERE":
        await message.reply("PLACE YOUR RESPONSE HERE") # Add more responses if needed
    elif content == "tell me a joke":
        # Send a random joke setup
        import random
        joke_id = random.choice(list(jokes.keys()))  # Pick a random joke
        await message.channel.send(jokes[joke_id]["setup"])
        # Track that the bot is waiting for a "why" response from this user for this specific joke
        joke_state[message.author.id] = joke_id
    elif content in ["why", "why?"] and joke_state.get(message.author.id, False):
        # Send the punchline for the specific joke
        joke_id = joke_state[message.author.id]
        await message.channel.send(jokes[joke_id]["punchline"])
        # Reset the state for this user
        joke_state[message.author.id] = False

    # Allow commands to work alongside the on_message event
    await bot.process_commands(message)

# Test command for Logs
@bot.command()
async def testlog(ctx):
    """
    Test the send_log function independently.
    Usage: ?testlog
    """
    # Simulate a moderation action
    action = "Test Action"
    member = ctx.author  # Use the command invoker as the member
    reason = "This is a test reason"
    duration = "5 minutes"

    # Call the send_log function
    await send_log(ctx, action, member, reason, duration)
    await ctx.send("Test log sent. Check the log channel and console output.")

# Send Logs to channel
async def send_log(ctx, action: str, member: discord.Member, reason: str = None, duration: str = None):
    """
    Send a log message to the log channel.
    """
    try:
        # Debug: Print all inputs
        print(f"[DEBUG] Logging action: {action}")
        print(f"[DEBUG] Member: {member.name} (ID: {member.id})")
        print(f"[DEBUG] Reason: {reason}")
        print(f"[DEBUG] Duration: {duration}")
        print(f"[DEBUG] Log Channel ID: {LOG_CHANNEL_ID}")

        # Get the log channel
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            print(f"[ERROR] Log channel with ID {LOG_CHANNEL_ID} not found.")
            return

        # Debug: Print log channel details
        print(f"[DEBUG] Log Channel Name: {log_channel.name}")
        print(f"[DEBUG] Log Channel Type: {log_channel.type}")
        print(f"[DEBUG] Bot Permissions in Channel: {log_channel.permissions_for(ctx.guild.me)}")

        # Check if the bot has permission to send messages in the log channel
        if not log_channel.permissions_for(ctx.guild.me).send_messages:
            print(f"[ERROR] Bot does not have permission to send messages in {log_channel.name}.")
            return

        # Format the reason in a code block
        formatted_reason = f"```{reason}```" if reason else "No reason provided"

        # Create the embed
        embed = discord.Embed(
            title=f"Action: {action}",
            description=f"**User:** {member.mention}\n**Moderator:** {ctx.author.mention}\n**Reason:** {formatted_reason}\n**Duration:** {duration}",
            color=discord.Color.red() if action in ["Ban", "Kick", "Mute"] else discord.Color.green()
        )

        # Debug: Print embed details
        print(f"[DEBUG] Embed Title: {embed.title}")
        print(f"[DEBUG] Embed Description: {embed.description}")

        # Try sending the embed
        try:
            await log_channel.send(embed=embed)
            print(f"[DEBUG] Log sent to channel {log_channel.name} ({log_channel.id})")
        except discord.Forbidden:
            # Fallback: Send a plain text message if embeds are not allowed
            log_message = (
                f"**Action:** {action}\n"
                f"**User:** {member.mention}\n"
                f"**Moderator:** {ctx.author.mention}\n"
                f"**Reason:** {formatted_reason}\n"
                f"**Duration:** {duration}"
            )
            await log_channel.send(log_message)
            print(f"[DEBUG] Fallback log sent to channel {log_channel.name} ({log_channel.id})")
        except Exception as e:
            print(f"[ERROR] Failed to send log message: {e}")

    except Exception as e:
        print(f"[ERROR] An error occurred while sending the log: {e}")    

# Command: Ban a user
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """
    Ban a user from the server.
    Usage: ?ban <user> [reason]
    """
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention} Reason: {reason}")

    # Call the send_log function
    await send_log(ctx, "Ban", member, reason)

# Command: Kick a user
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """
    Kick a user from the server.
    Usage: ?kick <user> [reason]
    """
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention} Reason: {reason}")

    # Call the send_log function
    await send_log(ctx, "Kick", member, reason)
    
# Command: Mute a user with a timer
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: int, unit: str = "minutes", *, reason=None):
    """
    Mute a user in the server for a specified duration.
    Usage: ?mute <user> <duration> [unit] [reason]
    """
    try:
        # Convert duration to seconds based on the unit
        unit = unit.lower()
        if unit == "min":
            duration_seconds = duration * 60
        elif unit == "hours":
            duration_seconds = duration * 3600
        elif unit == "days":
            duration_seconds = duration * 86400
        elif unit == "weeks":
            duration_seconds = duration * 604800
        elif unit == "months":
            duration_seconds = duration * 2592000  # Approximate: 30 days per month
        else:
            await ctx.send("Invalid unit. Supported units: minutes, hours, days, weeks, months")
            return

        # Find or create a "Muted" role
        muted_role = get(ctx.guild.roles, name="Muted")
        if not muted_role:
            # Create the "Muted" role if it doesn't exist
            muted_role = await ctx.guild.create_role(name="Muted", reason="Created for muting users")
            
            # Loop through all text channels and deny send messages permission for the "Muted" role
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(muted_role, send_messages=False, add_reactions=False)

        # Add the "Muted" role to the user
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"Muted {member.mention} for {duration} {unit}. Reason: {reason}")

        # Call the send_log function
        await send_log(ctx, "Mute", member, reason, f"{duration} {unit}")

        # Wait for the specified duration
        await asyncio.sleep(duration_seconds)

        # Remove the "Muted" role after the timer expires
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"Unmuted {member.mention} after {duration} {unit}.")

    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred while muting the user. Please check the bot's permissions and role hierarchy.")

# Command: Unmute a user
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    """
    Unmute a user in the server.
    Usage: ?unmute <user>
    """
    try:
        muted_role = get(ctx.guild.roles, name="Muted")
        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"Unmuted {member.mention}")

            # Call the send_log function
            await send_log(ctx, "Unmute", member)
        else:
            await ctx.send(f"{member.mention} is not muted.")

    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred while unmuting the user. Please check the bot's permissions and role hierarchy.")   

# Command: Warn a user
@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    """
    Warn a user in the server.
    Usage: ?warn <user> [reason]
    """
    await ctx.send(f"Warned :warning: {member.mention} Reason: {reason}")

    # Call the send_log function
    await send_log(ctx, "Warn", member, reason)

# Command: Clear a specified number of messages
@bot.command()
@commands.has_permissions(manage_messages=True)  # Restrict to users with "Manage Messages" permission
async def clear(ctx, amount: int):
    """
    Deletes a specified number of messages.
    Usage: ?clear <number>
    """
    if amount <= 0:
        await ctx.send("Please specify a number greater than 0")
        return

    # Delete the messages
    await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message itself
    await ctx.send(f"Cleared {amount} messages", delete_after=3)  # Delete the confirmation message after 3 seconds

# Command: Check bot latency (ping)
@bot.command()
async def ping(ctx):
    """
    Check the bot's latency.
    Usage: ?ping
    """
    latency = round(bot.latency * 1000)  # Convert latency to milliseconds
    await ctx.send(f"da latency is: **{latency}ms**")
    await ctx.send("Am i fast enough?")

# Error handling for the latency command
@ping.error
async def ping_error(ctx, error):
    await ctx.send("An error occurred while checking the latency. Please try again later.")

# Error handling for the clear command
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the number of messages to clear. Usage: `?clear <number>`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please provide a valid number. Usage: `?clear <number>`")

# Error handling for moderation commands
@ban.error
@mute.error
@unmute.error
@kick.error
@warn.error
async def moderation_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a user to perform this action.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid user specified.")
        
# Run the bot
bot.run(TOKEN)
