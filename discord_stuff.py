import discord
import subprocess
import re
from discord.ext import commands

TOKEN = ""

activity = discord.Game(name="!help")

#client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
        
@bot.command(name='reddit', help='send random image from specified subreddit')
async def reddit(ctx, subreddit):
    s = str(subprocess.check_output(["python3", "red.py", subreddit, "100"], encoding="utf-8")).split("||")
    await ctx.send(s[0])
    await ctx.send(s[1])

@bot.command(name='gentoo', help='install gentoo')
async def gentoo(ctx):
    await ctx.send("install gentoo")

@bot.command(name='eg', help='okayeg!')
async def eg(ctx):
    await ctx.send("https://media.tenor.com/CZxSdiSPndsAAAAC/okayeg.gif")

@bot.command(name='source', help='link source github repo')
async def eg(ctx):
    await ctx.send("https://github.com/CuBeRJAN/discord-bot")

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
