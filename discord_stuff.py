import discord
from discord.utils import get
import subprocess
import re
from discord.ext import commands

# Pure spaghetti code ahead

TOKEN = "" 

ROLE_EMOJIS = [['🍎', "MacOS", 0xFF0000],
               ['🪟', "Windows", 0x0000FF],
               ['🐧', "GNU+Linux", 0xFFFFFF],
               ['✝️', "Křesťanství", 0xFFFFFF],
               ['☸️', "Buddhismus", 0xFFFFFF],
               ['☪️', "Islám", 0xFF0000],
               ['✡️', "Judaismus", 0xFFFFFF],
               ['😈', "Satanismus", 0xFF0000]]

ROLE_CHANNEL =  # Channel for setting roles (int)

NEWBIE_ROLE =  # Role ID for new members (int)

activity = discord.Game(name="!help")

#client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.add_roles(member.guild.get_role(NEWBIE_ROLE))

@bot.event
async def on_raw_reaction_add(payload):
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    user = payload.member
    if 'role:' in reaction.message.content and reaction.message.author == bot.user and user != bot.user:
        for role in ROLE_EMOJIS:
            if reaction.emoji == role[0]:
                role_name = role[1]
                role_color = role[2]
                check_for_duplicate = get(reaction.message.author.guild.roles, name=role_name)
        if check_for_duplicate is None: # if the role doesn't exist
            role = await reaction.message.author.guild.create_role(name=role_name, colour=discord.Colour(role_color))
        else:
            role = check_for_duplicate
        await user.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    guild = await bot.fetch_guild(payload.guild_id)
    user = await guild.fetch_member(payload.user_id)
    if 'role:' in reaction.message.content and reaction.message.author == bot.user and user != bot.user:
        for role in ROLE_EMOJIS:
            if reaction.emoji == role[0]:
                role_name = role[1]
                role_color = role[2]
                check_for_duplicate = get(reaction.message.author.guild.roles, name=role_name)
        if check_for_duplicate is None: # if the role doesn't exist
            role = await reaction.message.author.guild.create_role(name=role_name, colour=discord.Colour(role_color))
        else:
            role = check_for_duplicate
        await user.remove_roles(role)
            
@bot.command()
@commands.has_permissions(administrator=True)
async def make_role(ctx, text, *emojis):
    channel = bot.get_channel(ROLE_CHANNEL)
    msg = await channel.send(text)
    
    for emoji in emojis:
        await msg.add_reaction(emoji)

@bot.command(name='poll', help='poll "text here" :emoji1: :emoji2: (use unicode emojis)')
async def poll(ctx, text, *emojis):
    msg = await ctx.send(text)
    for emoji in emojis:
        await msg.add_reaction(emoji)
    
@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def server_id(ctx):
    print(ctx.channel.guild.id)

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def roles(ctx):
    print(", ".join([str(r.id) for r in ctx.guild.roles]))
    print(", ".join([str(r.name) for r in ctx.guild.roles]))
    

@bot.command(name='reddit', help='send random image from specified subreddit')
async def reddit(ctx, subreddit):
    s = str(subprocess.check_output(["python3", "red.py", subreddit, "100"], encoding="utf-8")).split("||")
    await ctx.send(s[0])
    await ctx.send(s[1])

@bot.command(name='gentoo', help='install gentoo', hidden=True)
async def gentoo(ctx):
    await ctx.send("install gentoo")

@bot.command(name='eg', help='okayeg!')
async def eg(ctx):
    await ctx.send("https://media.tenor.com/CZxSdiSPndsAAAAC/okayeg.gif")

@bot.command(name='source', help='link source github repo')
async def eg(ctx):
    await ctx.send("<https://github.com/CuBeRJAN/discord-bot>")

@bot.command(name='vtip', help='random vtip')
async def alik_vtip_cmd(ctx):
    await ctx.send(subprocess.check_output(["python3", "alik_vtip.py"], encoding="utf-8"))

@bot.command(name='bible', help="bible verse")
async def bverse(ctx, book, verse):
    await ctx.send(subprocess.check_output(["python3", "bible.py", book, verse], encoding="utf-8"))

@bot.command(name='ph', help="ph list for category list")
async def ph(ctx, is_list):
    if is_list == "list":
        out = str(subprocess.check_output(["python3", "phub.py", "list"], encoding="utf-8"))[:-1]
        await ctx.send(out)
    else:
        await ctx.send(subprocess.check_output(["python3", "phub.py", "category", is_list], encoding="utf-8"))
        
@bot.command(name='linux', help='copypasta')
async def linux_cmd(ctx):
    await ctx.send("""I'd just like to interject for a moment. What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.

Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called "Linux", and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.

There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called "Linux" distributions are really distributions of GNU/Linux.""")
    
bot.run(TOKEN)
