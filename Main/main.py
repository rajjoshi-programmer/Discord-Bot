import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Logging setup
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot setup
bot = commands.Bot(command_prefix='!', intents=intents)  

#handling event when our bot is ready to online
@bot.event
async def on_ready():
    print(f"[🛠️] <Your Bot Name> bot is now live and monitoring your server!")
    print(f"[📡] Status: Online | Bot Name: {bot.user.name}")

#welcoming our new member in server
@bot.event
async def on_member_join(member):
    await member.send(f"Hello {member.name}, welcome to the server. Feel free to reach out if you need help — <Your Bot Name> is online and ready.")
#abusing restriction
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    banned_words = ["#abusive words","https://"] 
    if any(word in message.content.lower() for word in banned_words):
        await message.delete()
        await message.channel.send(f"🤖 Beep! {message.author.mention}, <Bot Name> detected bad language/Links. Let's keep things clean ⚡")

    await bot.process_commands(message)

# introduction command 
@bot.command()
async def aboutBot(ctx):
    await ctx.send(
    "Hey there! 🤖 I'm **Your Bot Name**, your friendly server assistant!\n"
    "I'm here to help with moderation, answer commands, and keep your community fun and safe. ⚡\n"
    "Type `!wannaHelp` to see what I can do!"
)

# help command 
@bot.command()
async def wannaHelp(ctx):
    await ctx.channel.send(
    "🎮 General Commands\n"
    "`!wannahelp` — Show this help message\n"

    "`!mute` <for specific role> — I mute the member with this command\n"

    "`!kick` <for specific role> — I kick the member with this command \n"

    "`!ban`  <for specific role> — I ban the member with this command \n"


)
    
#poll command
@bot.command()
async def poll(ctx,*,question):
    embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.blue())
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

# assigning roles with specific feature
@bot.command()
@commands.has_role("Staff")  # Only users with 'Staff' role can use this
async def assign(ctx, member: discord.Member):
    role_name = "Staff"  # Role you want to assign
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role:
        await member.add_roles(role)  # Give the role to mentioned user
        await ctx.send(f"✅ {member.mention} is now assigned as **{role.name}**.")
    else:
        await ctx.send("⚠ Role doesn't exist.")


# Error handler
@assign.error
async def assign_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"🚫 You don't have permission to do this, {ctx.author.mention}.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠ Please mention a user: `!assign @user`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("⚠ Could not find that user. Mention them properly.")
    else:
        await ctx.send("❌ Something went wrong.")
        raise error  # for debugging
    
# for removing role 
@bot.command()
@commands.has_role("Staff")  # Only users with 'Staff' role can use this
async def remove(ctx, member: discord.Member):
    role_name = "Staff"  # Role you want to assign
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role:
        await member.remove_roles(role)  # Give the role to mentioned user
        await ctx.send(f"✅ {member.mention} is now removed from **{role.name}**.")
    else:
        await ctx.send("⚠ He/She doesn't have this role.")

# for banning members
@bot.command()
@commands.has_role("Staff")
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} has been banned.\n📝 Reason: {reason}")
    except:
        await ctx.send(f'⚠: Error Occured')
#for security
    if member == ctx.author or member == bot.user:
     return await ctx.send("😅 You can't do that.")
# for unbanning members 
@bot.command()
@commands.has_role("Staff")
async def unban(ctx, *, user: str,reason):
    banned_users = await ctx.guild.bans()
    for entry in banned_users:
        if f"{entry.user.name}#{entry.user.discriminator}" == user:
            await ctx.guild.unban(entry.user)
            await ctx.send(f"🔨 {user.mention} has now unbanned.\n📝 Reason: {reason}")
            return
    await ctx.send(f"⚠ Couldn't find anyone named `{user}` in ban list.")
# for kicking members
@bot.command()
@commands.has_role("Staff")
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"🔨 {member.mention} has now kicked from server.\n📝 Reason: {reason}")
    except:
        await ctx.send(f'⚠: Error Occured')
# for timeout a member 
@bot.command()
@commands.has_role("Staff")
async def mute(ctx, member: discord.Member, duration_minutes: int, *, reason: str = None):
    try:
         duration = datetime.timedelta(minutes=duration_minutes)
         await member.timeout(duration, reason=reason)
         await ctx.send(f'{member.mention} has been muted for {duration_minutes} minutes.')
    except:
        await ctx.send(f'⚠: Error Occured')



# Run bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)