import discord
from discord.ext import commands
import os


client = commands.Bot(command_prefix = "!", case_insensitive=True)



@client.command(pass_context=True)
@commands.has_role('Sanitation Engineers')
async def botstart(ctx):
    pid = os.popen('pgrep -f "PickupBotMain.py"').read()
    print(pid)
    pid = int(pid[0])
    if(pid <= 6):
        os.system('./run.sh')
        await ctx.send("Pickup Bot coming back online.. give it about 5 seconds..")
        await ctx.send(pid)
        os.system('pidof PickupBotMain.py')
    else:
        await ctx.send("Bot is already running..")

client.run('NzU3MDgzNTkyNzM1MDY0MTY2.X2bPCg.QOndInrTzUQQMwNJF1BpSsnUarI')