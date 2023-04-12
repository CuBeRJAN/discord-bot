import discord
from discord.utils import get
import subprocess
import re
import asyncio
from discord.ext import commands
import random
from typing import Union
from youtube_search import YoutubeSearch

# Pure spaghetti code ahead

TOKEN = ""

ROLE_EMOJIS = [['macos', "MacOS", 0xFF0000], # Hardcoding like this is pretty ugly
               ['windows', "Windows", 0x0000FF],
               ['linux', "GNU+Linux", 0xFFFFFF],
               ['✝️', "Křesťanství", 0xFFFFFF],
               ['☸️', "Buddhismus", 0xFFFFFF],
               ['☪️', "Islám", 0xFF0000],
               ['✡️', "Judaismus", 0xFFFFFF],
               ['😈', "Satanismus", 0xFF0000],
               ['minecraft', "Minecraft", 0x00FF00],
               ['lol', "League of Legends", 0xFFD700],
               ['csgo', "CS: GO", 0xFFFFFF],
               ['rbr', "RBR", 0xFFA500],
               ['valorant', "Valorant", 0xFF0000],
               ['emacs', "Emacs", 0xA020F0],
               ['vscode', "VS Code", 0x0000FF],
               ['vim', "Vim", 0x00FF00],
               ['🟣', "Fialová", 0xB053F3],
               ['🔴', "Červená", 0xFF0000],
               ['⚪', "Bílá", 0xFFFFFF],
               ['🟢', "Zelená", 0x00FF00],
               ['🔵', "Modrá", 0x4444FF],
               ['⚫', "Černá", 0x000001],
               ['🔞', "NSFW", 0xFF0000]
               ]

BANNED_WORDS = ["sieg ", "heil hitler", "nigg", "fagg", "negr ", "nigr "] # space at the end means the string can be used as part of another word
NUMBER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
CANCEL_EMOJI = "❌"

ROLE_CHANNEL =  # Channel for setting roles (int)
ASSIGN_CHANNEL =  # Channel for assigning role emojis

NEWBIE_ROLE =  # Role ID for new members (int)

activity = discord.Game(name="!help")

#client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)

async def s_check(ctx, cmd, encoding="utf-8", timeout=15):
    try:
        return subprocess.check_output(cmd, encoding=encoding, timeout=timeout)
    except subprocess.TimeoutExpired:
        await ctx.send("timeout error")
        return

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
    if member.guild.id == :
        await member.add_roles(member.guild.get_role(NEWBIE_ROLE))

@bot.event
async def on_message(message):
    process = True
    for word in BANNED_WORDS: # iterate list
        if word in message.content.casefold():
            await message.delete()
            process = False
            break
        s = message.content.split()
        if " " in word and len(s) > 0 and len(s) < 2:
            if word.strip() == s[0]:
                await message.delete()
                process = False
                break
    if process: # all checks passed!
        await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != ROLE_CHANNEL: # Since the only function here is for roles we can skip reactions that aren't in the role channel
        return
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if not message:
        return
    emoji = discord.utils.get(message.guild.emojis, name=payload.emoji.name)
    if emoji:
        emoji_s = payload.emoji.name
    else:
        emoji = payload.emoji.name
        emoji_s = emoji
    reaction = discord.utils.get(message.reactions, emoji=emoji)
    user = payload.member
    if reaction and reaction.message and ('role:' in reaction.message.content and reaction.message.author == bot.user and user != bot.user):
        for role in ROLE_EMOJIS:
            if emoji_s == role[0]:
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
    if payload.channel_id != ROLE_CHANNEL:
        return
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if not message:
        return
    emoji = discord.utils.get(message.guild.emojis, name=payload.emoji.name)
    if emoji:
        emoji_s = payload.emoji.name
    else:
        emoji = payload.emoji.name
        emoji_s = emoji
    reaction = discord.utils.get(message.reactions, emoji=emoji)
    guild = await bot.fetch_guild(payload.guild_id)
    user = await guild.fetch_member(payload.user_id)
    if reaction and reaction.message and ('role:' in reaction.message.content and reaction.message.author == bot.user and user != bot.user):
        for role in ROLE_EMOJIS:
            if emoji_s == role[0]:
                role_name = role[1]
                role_color = role[2]
                check_for_duplicate = get(reaction.message.author.guild.roles, name=role_name)
        if check_for_duplicate is None: # if the role doesn't exist
            role = await reaction.message.author.guild.create_role(name=role_name, colour=discord.Colour(role_color))
        else:
            role = check_for_duplicate
        await user.remove_roles(role)

@bot.command(hidden=True)
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

@bot.command(name='yt', help='youtube search')
async def yt(ctx, *terms):
    def check(r: discord.Reaction, u: Union[discord.Member, discord.User]):
        return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and \
               (str(r.emoji) in NUMBER_EMOJIS or str(r.emoji) == CANCEL_EMOJI)
    
    results = YoutubeSearch(" ".join(terms), max_results=5).to_dict()
    r_str = "pick a result:\n```\n"
    i = 0
    for v in results:
        title = v['title']
        duration = v['duration']
        maxlen = 60
        while len(title) < maxlen:
            title += " "
        if len(title) > maxlen:
            title = title[0:maxlen-3]
            title += "..."
        while len(duration) < 7:
            duration += " "
        r_str += f"{title} || {duration} || {NUMBER_EMOJIS[i]}\n"
        i += 1
    msg = await ctx.send(r_str + "```")
    await msg.add_reaction(CANCEL_EMOJI)
    for emoji in NUMBER_EMOJIS:
        await msg.add_reaction(emoji)
    try:
        reaction, user = await bot.wait_for('reaction_add', check = check, timeout = 60.0)
    except asyncio.TimeoutError:
        await ctx.send(f"**{ctx.author}**, you didnt react in 60 seconds.")
        return
    else:
        if reaction.emoji == CANCEL_EMOJI:
            await msg.delete()
            return
        for emoji in NUMBER_EMOJIS:
            if reaction.emoji == emoji:
                i = NUMBER_EMOJIS.index(emoji)
                await msg.delete()
                await ctx.send("https://youtube.com" + results[i]["url_suffix"])

@bot.command(name='chords') # Very ugly
async def chords(ctx, scale, n=4):
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    letters = ["A", "B", "C", "D", "E", "F", "G"]
    minor = [2, 1, 2, 2, 1, 2]
    major = [2, 2, 1, 2, 2, 2]
    if "#" not in scale and "b" not in scale:
        root = scale[0]
    else:
        root = scale[0] + scale[1]
    d_notes = notes + notes
    d_letters = letters + letters
    root_s = ["#", "#"]
    if "b" in root: # Convert flats to appropriate sharps
        root_s[0] = letters[letters.index(root[0])-1]
        root_s[1] = "#"
        root = "".join(root_s)
    if root not in notes:
        await ctx.send("to není skutečná nota")
        return
    root_i = notes.index(root)
    s = major
    if len(scale) > 1 and scale[-1] == 'm':
        s = minor
    i = 0
    f_scale = [root]
    for interval in s: # Append intervals to create scale
        i += interval
        f_scale.append(d_notes[root_i + i])
    chords = []
    for i in range(0, len(f_scale), +1): # Append chords
        minor_third = d_notes[d_notes.index(f_scale[i])+3]
        major_third = d_notes[d_notes.index(f_scale[i])+4]
        minor_seventh = d_notes[d_notes.index(f_scale[i])+10]
        major_seventh = d_notes[d_notes.index(f_scale[i])+11]
        fifth = d_notes[d_notes.index(f_scale[i])+7]
        diminished_fifth = d_notes[d_notes.index(f_scale[i])+6]
        if minor_third in f_scale and fifth in f_scale: # minor
            chords.append(str(f_scale[i] + "m"))
        if major_third in f_scale and fifth in f_scale: # major
            chords.append(str(f_scale[i]))
        if minor_third in f_scale and diminished_fifth in f_scale: # diminished
            chords.append(str(f_scale[i] + "dim"))
        if minor_third in f_scale and diminished_fifth in f_scale and minor_seventh in f_scale: # diminished seventh
            chords.append(str(f_scale[i] + "dim7"))
        if minor_third in f_scale and minor_seventh in f_scale: # minor seventh
            chords.append(str(f_scale[i] + "m7"))
        if major_third in f_scale and major_seventh in f_scale: # major seventh
            chords.append(str(f_scale[i] + "7"))
    prog = []
    choice = ""
    for i in range(0, n, +1):
        n_choice = random.choice(chords)
        while choice == n_choice:
            n_choice = random.choice(chords)
        choice = n_choice
        prog.append(choice)
    await ctx.send("chord progression in the key of " + scale + ": " + " ".join(prog))
    
@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def server_id(ctx):
    print(ctx.channel.guild.id)

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def roles(ctx):
    print(", ".join([str(r.id) for r in ctx.guild.roles]))
    print(", ".join([str(r.name) for r in ctx.guild.roles]))

@bot.command(name='alignment')
async def alignment(ctx):
    a_0 = ["lawful", "chaotic", "neutral"]
    a_1 = ["evil", "good", "neutral"]
    if a_0 == "neutral" and a_1 == "neutral":
        a_0 = "true"
    await ctx.send(f"{random.choice(a_0)} {random.choice(a_1)}")

@bot.command(name='reddit', help='send random image from specified subreddit')
async def reddit(ctx, subreddit):
    nsfw = "sfw"
    if ctx.channel.is_nsfw():
        nsfw = "nsfw"
    s = str(await s_check(ctx, ["python3", "red.py", subreddit, "100", nsfw], encoding="utf-8", timeout=15)).split("||")
    await ctx.send(s[0])
    if len(s)>1:
        await ctx.send(s[1])

@bot.command(name='gentoo', help='install gentoo', hidden=True)
async def gentoo(ctx):
    await ctx.send("install gentoo")

@bot.command(name='choice', help='random choice')
async def choice(ctx, *choices):
    await ctx.send(random.choice(choices))

@bot.command(name='eg', hidden=True)
async def eg(ctx):
    await ctx.send("https://media.tenor.com/CZxSdiSPndsAAAAC/okayeg.gif")

@bot.command(name='word')
async def word(ctx, *words):
    s = ["figlet"] + list(words)
    await ctx.send("```\n" + (await s_check(ctx, s, encoding="utf-8")) + "\n```")

@bot.command(name='cowsay')
async def cowsay(ctx, *words_t):
    if not words_t:
        await ctx.send("Dostupná zvířátka: ``(!cowsay -f zviratko text)`` ```\n" + (await s_check(ctx, ["cowsay", "-l"], encoding="utf-8").replace('\n', ", ")) + "```\n")
        return
    words = list(words_t)
    for i in range(0, len(words), +1):
        words[i] = words[i].replace("'","\'").replace('""', '\"')
    if 'sodomized' in words and not ctx.channel.is_nsfw():
        await ctx.send("That cowsay is a bit too nsfw!")
        return
    s = ["cowsay"] + list(words)
    await ctx.send("```\n" + (await s_check(ctx, s, encoding="utf-8")) + "\n```")

@bot.command(name='fortune')
async def fortune(ctx):
    s = ["fortune"]
    await ctx.send("```\n" + (await s_check(ctx, s, encoding="utf-8")) + "\n```")

@bot.command(name='cowfortune')
async def fortune(ctx):
    fortune = await s_check(ctx, ["fortune"], encoding="utf-8")
    s = ["cowsay"] + fortune.split()
    await ctx.send("```\n" + (await s_check(ctx, s, encoding="utf-8")) + "\n```")

@bot.command(name='cowvtip', help='random vtip')
async def alik_vtip_cmd(ctx):
    vtip = await s_check(ctx, ["python3", "alik_vtip.py"], encoding="utf-8")
    s = ["cowsay"] + vtip.split()
    await ctx.send("```\n" + (await s_check(ctx, s, encoding="utf-8")) + "\n```")

@bot.command(name='source', help='link source github repo')
async def eg(ctx):
    await ctx.send("<https://github.com/CuBeRJAN/discord-bot>")

@bot.command(name='vtip', help='random vtip')
async def alik_vtip_cmd(ctx):
    await ctx.send(await s_check(ctx, ["python3", "alik_vtip.py"], encoding="utf-8"))

@bot.command(name='bible', help="bible verse")
async def bverse(ctx, book, verse):
    await ctx.send(await s_check(ctx, ["python3", "bible.py", book, verse], encoding="utf-8"))

@bot.command(name='ph', help="ph list for category list")
async def ph(ctx, is_list):
    if ctx.channel.is_nsfw():
        if is_list == "list":
            out = str(await s_check(ctx, ["python3", "phub.py", "list"], encoding="utf-8"))[:-1]
            await ctx.send(out)
        elif is_list == "fav":
            await ctx.send("Tvůj oblíbený typ porna je " + await s_check(ctx, ["python3", "phub.py", "rand"], encoding="utf-8"))
        else:
            await ctx.send(await s_check(ctx, ["python3", "phub.py", "category", is_list], encoding="utf-8"))
    else:
        await ctx.send("This command can only be used in NSFW channels.")
        
@bot.command(name='linux', help='copypasta', hidden=True)
async def linux_cmd(ctx):
    await ctx.send("""I'd just like to interject for a moment. What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.

Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called "Linux", and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.

There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called "Linux" distributions are really distributions of GNU/Linux.""")
    
bot.run(TOKEN)
