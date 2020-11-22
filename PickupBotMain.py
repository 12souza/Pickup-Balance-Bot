import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import discord
from discord.ext import commands
from rHLDS import Console
import math
import random
import itertools
with open('players.json') as f:
  playerRanks = json.load(f)

with open('notifyList.json') as f:
  notifyList = json.load(f)

#GLOBALS 
totalPlayers = []
msg = " "
eList = []
msgList = ['     │     Player Name            │\n', '=====╪============================╪==\n']
pickupLeader = " "
blueTeam = []
redTeam = []
pickupActive = 0
playerIDs = {}
autoPickupActive = 0
pickupCount = 0
thxPickupActive = 0
rTotalPlayers = {}
bVoiceList = []
rVoiceList = []


#RCON SERVER INFORMATION
srv = Console(host='192.223.26.130', password='rational')
#srv = Console(host='localhost', password='hello')
srv.connect()

#Google API Stuff
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("playerbot.json", scope)
gClient = gspread.authorize(creds)
sheet = gClient.open("players").sheet1

#DISCORD API
client = commands.Bot(command_prefix = "!", case_insensitive=True)

#FUNCTIONS
def findPlayerRow(player):
    find = str(sheet.find(player))
    findList = find.split()
    if(len(findList[1]) == 4):    
        row = int(findList[1][1])
    elif(len(findList[1]) == 5):
        row = int(findList[1][1:3])
    elif(len(findList[1]) == 6):
        row = int(findList[1][1:4])

    return row

def PopulateTable():
    global msgList
    global totalPlayers
    global eList
    global msg

    eList = list(enumerate(list(rTotalPlayers), start=1))
    del msgList[2:-1]
    if(len(msgList) > 2):
        del msgList[2]
    for i in range(len(eList)):
        
        msgList.append("  " + str(eList[i][0]) + " " * (3 - len(str(eList[i][0]))) + "│ " + eList[i][1] + (" " * (27 - len(eList[i][1]))) + "│\n")

    
    msg = ''.join(msgList)
    return msg

def DePopulatePickup():
    global pickupActive
    global totalPlayers
    global redTeam 
    global blueTeam
    global pickupLeader 
    global pickupActive
    global playerIDs
    global autoPickupActive
    global pickupCount
    global thxPickupActive 
    global rTotalPlayers

    autoPickupActive = 0
    pickupActive = 0
    redTeam = []
    blueTeam = []
    totalPlayers = []
    pickupLeader = None
    pickupActive = 0
    playerIDs = {}
    pickupCount = 0
    thxPickupActive = 0
    rTotalPlayers = {}
    bVoiceList = []
    rVoiceList = []

#BOT COMMANDS FOR SECRET CHANNEL
@client.command(pass_context=True)
@commands.has_role('SECRET COMMITTEE MEMBERS')
async def rating(ctx, player):
    row = findPlayerRow(player)
    average = sheet.cell(row, 8).value
    await ctx.send(player + " has an average rating of " + average + ".")



@client.command(pass_context=True)
@commands.has_role('SECRET COMMITTEE MEMBERS')
async def rate(ctx, player, value: int):
    if (value < 1) or (value > 10):
        await ctx.send("Invalid value, please rate 1-10") 
    else:   
        row = findPlayerRow(player)
        if(ctx.author.id == 118900492607684614):
            sheet.update_cell(row, 3, value)
        if(ctx.author.id == 308261407047024641):
            sheet.update_cell(row, 4, value)
        if(ctx.author.id == 618946434569470004):
            sheet.update_cell(row, 5, value)
        if(ctx.author.id == 700549591413555242):
            sheet.update_cell(row, 6, value)
        if(ctx.author.id == 90535428821622784):
            sheet.update_cell(row, 3, value)
        await ctx.send("Your rating for " + player + " has been updated to " + str(value) + ".")

@client.command(pass_context=True)
@commands.has_role('SECRET COMMITTEE MEMBERS')
async def myrating(ctx, player):
    if(ctx.channel.name == "secret-bot-stuff-dont-open"):    
        row = findPlayerRow(player)
        if(ctx.author.id == 118900492607684614):
            value = sheet.cell(row, 3).value
        if(ctx.author.id == 308261407047024641):
            value = sheet.cell(row, 4).value
        if(ctx.author.id == 618946434569470004):
            value = sheet.cell(row, 5).value
        if(ctx.author.id == 700549591413555242):
            value = sheet.cell(row, 6).value
        if(ctx.author.id == 90535428821622784):
            value = sheet.cell(row, 7).value
        await ctx.send("Your rating for " + player + " is " + str(value) + ".")

@client.command(pass_context=True)
async def timeleft(ctx):
    mSeconds = srv.execute("mp_timeleft")
    lSeconds = mSeconds.split()
    mRound = srv.execute("currentRound")
    lRound = mRound.split()
    tRound = lRound[2]
    mMap = srv.execute("currentmap")
    lMap = mMap.split()
    tMap = lMap[2]
    cfg = srv.execute("outhousefull")
    cfgSplit = cfg.split()
    servercfg = cfgSplit[2]
    cfgname = servercfg[1]
    t1 = srv.execute("BlueScore")
    t1s = t1.split()
    t1i = t1s[2]
    teamOneScore = t1i[1:-1]
    t2 = srv.execute("RedScore")
    t2s = t2.split()
    t2i = t2s[2]
    teamTwoScore = t2i[1:-1]
    tp = srv.execute("previousscore")
    tps = tp.split()
    tpi = tps[2]
    prevScore = tpi[1:-1]

    print(lSeconds[2])
    if(len(lSeconds[2]) == 5):
        tSeconds = lSeconds[2][1:4]
    elif(len(lSeconds[2]) == 6):
        tSeconds = lSeconds[2][1:5]
    elif(len(lSeconds[2]) == 4):
        tSeconds = lSeconds[2][1:3]
    elif(len(lSeconds[2]) == 3):
        tSeconds = lSeconds[2][1]

    minutes = int(tSeconds) // 60
    seconds = int(tSeconds) % 60

    if(cfgname == "0"):
        if(tRound[1] == "1"):
            if(seconds >= 10):  
                await ctx.send("```Round " + str(tRound)[1] 
                + "\nCurrent Map: " + tMap[1:-1]
                + "\nTimeleft: " + str(minutes) + ':' + str(seconds)
                + "\nTeam 1 Score (OFFENSE): " + teamOneScore
                + "\nTeam 2 Score (DEFENSE): TBA```")
            else:
                await ctx.send("```Round " + str(tRound)[1] 
                + "\nCurrent Map: " + tMap[1:-1]
                + "\nTimeleft: " + str(minutes) + ':0' + str(seconds)
                + "\nTeam 1 Score (OFFENSE): " + teamOneScore
                + "\nTeam 2 Score (DEFENSE): TBA```")
        else:
            if(seconds >= 10):  
                await ctx.send("```Round " + str(tRound)[1] 
                + "\nCurrent Map: " + tMap[1:-1]
                + "\nTimeleft: " + str(minutes) + ':' + str(seconds)
                + "\nTeam 1 Score (DEFENSE): " + prevScore
                + "\nTeam 2 Score (OFFENSE): " + teamOneScore + "```")
            else:
                await ctx.send("Round " + str(tRound)[1] + " - " + str(minutes) + ':0' + str(seconds) + " - Current Map: " + tMap[1:-1])
                await ctx.send("```Round " + str(tRound)[1] 
                + "\nCurrent Map: " + tMap[1:-1]
                + "\nTimeleft: " + str(minutes) + ':0' + str(seconds)
                + "\nTeam 1 Score (DEFENSE): " + prevScore
                + "\nTeam 2 Score (OFFENSE): " + teamOneScore + "```")
    elif(cfgname == "1"):
        if(seconds >= 10):  
            await ctx.send("```Round " + str(tRound)[1] 
            + "\nCurrent Map: " + tMap[1:-1]
            + "\nTimeleft: " + str(minutes) + ':' + str(seconds)
            + "\nTeam 1 Score: " + teamOneScore
            + "\nTeam 2 Score: " + teamTwoScore + "```")
        else:
            await ctx.send("Round " + str(tRound)[1] + " - " + str(minutes) + ':0' + str(seconds) + " - Current Map: " + tMap[1:-1])
            await ctx.send("```Round " + str(tRound)[1] 
            + "\nCurrent Map: " + tMap[1:-1]
            + "\nTimeleft: " + str(minutes) + ':0' + str(seconds)
            + "\nTeam 1 Score: " + teamOneScore
            + "\nTeam 2 Score: " + teamTwoScore + "```")

@client.command(pass_context=True)
async def notifyme(ctx):
    with open('notifyList.json') as f:
        notifyList = json.load(f)
    
    if ctx.author.id not in notifyList:
        notifyList.append(ctx.author.id)
        await ctx.send("You have been added to the Pickup Notification List.  You will receive a DM everytime a pickup games begins at the outhouse")
    else:
        await ctx.send("You are already in the notification list :)")
    with open('notifyList.json', 'w') as fp:
        json.dump(notifyList, fp,indent= 4)

@client.command(pass_context=True)
async def unnotifyme(ctx):
    with open('notifyList.json') as f:
        notifyList = json.load(f)
    
    if ctx.author.id in notifyList:
        notifyList.remove(ctx.author.id)
        await ctx.send("You have removed yourself from the notification list")
    else:
        await ctx.send("You are not in the notification list")

    with open('notifyList.json', 'w') as fp:
        json.dump(notifyList, fp,indent= 4)

@client.command(pass_context=True)
@commands.has_role('Sanitation Engineers')
async def amx_map(ctx, mapname):
    if(ctx.channel.name == "sanitation-engineers"):    
        amxcommand = "amx_map " + mapname
        srv.execute(amxcommand)

@client.command(pass_context=True)
@commands.has_role('Sanitation Engineers')
async def amx_cfg(ctx, cfgname):
    if(ctx.channel.name == "sanitation-engineers"):    
        amxcommand = "amx_cfg " + cfgname
        srv.execute(amxcommand)

@client.command(pass_context=True)
@commands.has_role('SECRET COMMITTEE MEMBERS')
async def amx_say(ctx, message):
    if(ctx.channel.name == "secret-bot-stuff-dont-open"):    
        amxcommand = "amx_say " + message
        srv.execute(amxcommand)

#BOT COMMANDS FOR PICKUP
@client.command(pass_context=True)
@commands.has_role('Sanitation Engineers')
async def pickup(ctx):
    global playerIDs
    global pickupLeader
    global pickupActive
    global rTotalPlayers

    row = findPlayerRow(str(ctx.author.id))
    playerName = sheet.cell(row, 2).value
    playerRating = sheet.cell(row, 8).value
    occ = srv.execute("occupied")
    occSplit = occ.split()
    occupied = occSplit[2]

    if(occupied == '"0"'):
        if(autoPickupActive == 0) and (thxPickupActive == 0):    
            if(ctx.channel.name == 'outhouse-pickups'):    
                if(pickupActive == 0):
                    DePopulatePickup()
                    pickupLeader = ctx.author.display_name
                    await ctx.send("```A pickup has been started by " + pickupLeader + ".  Please type '!add' to join the pickup game..```")

                    playerIDs[playerName] = ctx.author.id
                    rTotalPlayers[playerName] = playerRating
                    PopulateTable()
                    await ctx.send("```" + msg + "```")
                    pickupActive = 1
                else:
                    await ctx.send("There is already an active pickup.. please !add to that..")
        else:
            await ctx.send("Team Auto currently has a pickup active...")
    else:
        await ctx.send("The Outhouse is currently occupied and will be available later")

@client.command(pass_context=True,)
@commands.has_role('auto!')
async def autopickup(ctx, size):
    global playerIDs
    global autoPickupActive
    global pickupCount

    if((pickupActive == 0) and (thxPickupActive == 0)):    
        if(ctx.message.channel.name == 'outhouse-pickups'):    
            if(autoPickupActive == 0):
                DePopulatePickup()
                blueTeam.append(ctx.author.display_name)
                await ctx.send("```Come play against auto!  type !add to join!````")

                bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                bEnumList = list(enumerate(blueTeam, start = 1))
                for i in range(len(bEnumList)):
                    bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│\n")
                bMsg = ''.join(bMsgList)

                rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                rEnumList = list(enumerate(redTeam, start = 1))
                for i in range(len(rEnumList)):
                    rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│\n")
                rMsg = ''.join(rMsgList)

                await ctx.send("These are the teams\n\n  **Team auto!**" + "```" + bMsg + "```\n\n\n**Team Outhouse**\n" +"```" + rMsg + "```")
                autoPickupActive = 1
                pickupCount = size
    else:
        await ctx.send("Currently a Pickup Active")

@client.command(pass_context=True,)
@commands.has_role('thx,')
async def thxpickup(ctx, size):
    global playerIDs
    global thxPickupActive
    global pickupCount

    if((pickupActive == 0) and (autoPickupActive == 0)):    
        if(ctx.message.channel.name == 'outhouse-pickups'):    
            if(thxPickupActive == 0):
                DePopulatePickup()
                blueTeam.append(ctx.author.display_name)
                await ctx.send("```Come play against auto!  type !add to join!````")

                bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                bEnumList = list(enumerate(blueTeam, start = 1))
                for i in range(len(bEnumList)):
                    bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│\n")
                bMsg = ''.join(bMsgList)

                rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                rEnumList = list(enumerate(redTeam, start = 1))
                for i in range(len(rEnumList)):
                    rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│\n")
                rMsg = ''.join(rMsgList)

                await ctx.send("The game is ready to begin!\n\n  **Team thx,**" + "```" + bMsg + "```\n\n\n**Team Outhouse**\n" +"```" + rMsg + "```")
                thxPickupActive = 1
                pickupCount = size
    else:
        await ctx.send("Currently a Pickup Active")

@client.command(pass_context=True)
async def add(ctx):
    global pickupActive
    global totalPlayers
    global playerIDs
    global pickupCount
    global autoPickupActive
    global thxPickupActive
    global rTotalPlayers
    global redTeam
    global blueTeam
    with open('players.json') as f:
        playerRanks = json.load(f)
    
    playerID = ctx.author.id
    playerName = ctx.author.display_name
    if(ctx.message.channel.name == 'outhouse-pickups'):    
        if(pickupActive == 1):   
            if (len(list(rTotalPlayers)) < 22):    
                if(playerName not in list(rTotalPlayers)):    
                    if(str(playerID) not in list(playerRanks)):
                        insertHere = len(sheet.col_values(1)) + 1
                        #average = "=ROUNDDOWN(AVERAGEA(C" + str(insertHere) + ":G" + str(insertHere) + "))"
                        insertRow = [str(playerID), playerName, 5, 5, 5, 5, 5, 5]
                        sheet.insert_row(insertRow, insertHere)
                        playerRanks[playerID] = [playerName, 5, 5, 5, 5, 5]
                        channel = client.get_channel(760160980738244628)

                        with open('players.json', 'w') as fp:
                            json.dump(playerRanks, fp,indent= 4)
                        await channel.send(playerName + " with the player ID (" + str(playerID) + ") has been added to the rating list and needs a rating." )
                    
                    row = findPlayerRow(str(ctx.author.id))
                    playerName = sheet.cell(row, 2).value
                    playerRating = sheet.cell(row, 8).value
                    
                    playerIDs[playerName] = playerID
                    rTotalPlayers[playerName] = playerRating
                    PopulateTable()

                    await ctx.send("```" + msg + "```")
                else:
                    await ctx.send("You're already in the pickup vato..")
            else:
                await ctx.send("Pickup is FULL")

        elif(autoPickupActive == 1):
            player = ctx.author.display_name
            roles = ctx.author.roles
            if((player not in blueTeam) and (player not in redTeam)):
                    
                if("auto!" not in str(roles)):
                    print(pickupCount, player, len(redTeam))
                    if(len(redTeam) < int(pickupCount)):
                        redTeam.append(player)
                        
                elif(("auto!" in str(roles)) and ((len(blueTeam) < int(pickupCount)))):
                    blueTeam.append(player)

                bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                bEnumList = list(enumerate(blueTeam, start = 1))
                for i in range(len(bEnumList)):
                    bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│\n")
                bMsg = ''.join(bMsgList)

                rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                rEnumList = list(enumerate(redTeam, start = 1))
                for i in range(len(rEnumList)):
                    rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│\n")
                rMsg = ''.join(rMsgList)

                await ctx.send("Here are the teams!\n\n  **Team auto!**" + "```" + bMsg + "```\n\n\n**Team Outhouse**\n" +"```" + rMsg + "```")
                if ((len(blueTeam) == int(pickupCount)) and (len(redTeam) == int(pickupCount))):
                    
                    if(int(pickupCount) == 2):
                        await ctx.send("!mapvote 2v2")
                    elif(int(pickupCount) == 3):
                        await ctx.send("!mapvote 3v3")
                    elif(int(pickupCount) == 4):
                        await ctx.send("!mapvote 4v4")
                    elif(int(pickupCount) == 5):
                        await ctx.send("!mapvote 5v5")
                    else:
                        await ctx.send("Could not determine format, please use !mapvote command")

                    await ctx.send("Your pickup is now ready, please put in your vote for the map and join the server at steam://connect/192.223.26.130:27015/janitor")
                    DePopulatePickup()
            else: 
                await ctx.send("You're already in this pickup vato")
        
        elif(thxPickupActive == 1):
            player = ctx.author.display_name
            roles = ctx.author.roles
            if((player not in blueTeam) and (player not in redTeam)):
                    
                if("auto!" not in str(roles)):
                    print(pickupCount, player, len(redTeam))
                    if(len(redTeam) < int(pickupCount)):
                        redTeam.append(player)
                        
                elif(("auto!" in str(roles)) and ((len(blueTeam) < int(pickupCount)))):
                    blueTeam.append(player)

                bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                bEnumList = list(enumerate(blueTeam, start = 1))
                for i in range(len(bEnumList)):
                    bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│\n")
                bMsg = ''.join(bMsgList)

                rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                rEnumList = list(enumerate(redTeam, start = 1))
                for i in range(len(rEnumList)):
                    rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│\n")
                rMsg = ''.join(rMsgList)

                await ctx.send("Here are the teams!\n\n  **Team auto!**" + "```" + bMsg + "```\n\n\n**Team Outhouse**\n" +"```" + rMsg + "```")
                if ((len(blueTeam) == int(pickupCount)) and (len(redTeam) == int(pickupCount))):
                    
                    if(int(pickupCount) == 2):
                        await ctx.send("!mapvote 2v2")
                    elif(int(pickupCount) == 3):
                        await ctx.send("!mapvote 3v3")
                    elif(int(pickupCount) == 4):
                        await ctx.send("!mapvote 4v4")
                    elif(int(pickupCount) == 5):
                        await ctx.send("!mapvote 5v5")
                    else:
                        await ctx.send("Could not determine format, please use !mapvote command")

                    await ctx.send("Your pickup is now ready, please put in your vote for the map and join the server at steam://connect/192.223.26.130:27015/janitor")
                    DePopulatePickup()
            else: 
                await ctx.send("You're already in this pickup vato")
        else:
           await ctx.send("No pickup active..") 

@client.command(pass_context=True)
@commands.has_role('Sanitation Engineers')
async def addplayer(ctx, name):
    global pickupActive
    global totalPlayers
    global playerIDs
    global pickupCount
    global autoPickupActive
    global thxPickupActive
    global rTotalPlayers
    with open('players.json') as f:
        playerRanks = json.load(f)
    
    playerID = ctx.author.id
    playerName = ctx.author.display_name
    if(ctx.message.channel.name == 'outhouse-pickups'):    
        if(pickupActive == 1):   
            if(playerName not in list(rTotalPlayers)):    
                if(str(playerID) not in list(playerRanks)):
                    insertHere = len(sheet.col_values(1)) + 1
                    #average = "=ROUNDDOWN(AVERAGEA(C" + str(insertHere) + ":G" + str(insertHere) + "))"
                    insertRow = [str(playerID), playerName, 5, 5, 5, 5, 5, 5]
                    sheet.insert_row(insertRow, insertHere)
                    playerRanks[playerID] = [playerName, 5, 5, 5, 5, 5]
                    channel = client.get_channel(760160980738244628)

                    with open('players.json', 'w') as fp:
                        json.dump(playerRanks, fp,indent= 4)
                    await channel.send(playerName + " with the player ID (" + str(playerID) + ") has been added to the rating list and needs a rating." )
                
                row = findPlayerRow(str(ctx.author.id))
                playerName = sheet.cell(row, 2).value
                playerRating = sheet.cell(row, 8).value
                
                playerIDs[playerName] = playerID
                rTotalPlayers[playerName] = playerRating
                PopulateTable()

                await ctx.send("```" + msg + "```")
            else:
                await ctx.send("You're already in the pickup vato..")

        elif(autoPickupActive == 1):
            player = ctx.author.display_name
            roles = ctx.author.roles
            if((player not in blueTeam) and (player not in redTeam)):
                    
                if("auto!" not in str(roles)):
                    print(pickupCount, player, len(redTeam))
                    if(len(redTeam) < int(pickupCount)):
                        redTeam.append(player)
                        
                elif(("auto!" in str(roles)) and ((len(blueTeam) < int(pickupCount)))):
                    blueTeam.append(player)

                bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                bEnumList = list(enumerate(blueTeam, start = 1))
                for i in range(len(bEnumList)):
                    bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│\n")
                bMsg = ''.join(bMsgList)

                rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                rEnumList = list(enumerate(redTeam, start = 1))
                for i in range(len(rEnumList)):
                    rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│\n")
                rMsg = ''.join(rMsgList)

                await ctx.send("Here are the teams!\n\n  **Team auto!**" + "```" + bMsg + "```\n\n\n**Team Outhouse**\n" +"```" + rMsg + "```")
                if ((len(blueTeam) == int(pickupCount)) and (len(redTeam) == int(pickupCount))):
                    
                    if(int(pickupCount) == 2):
                        await ctx.send("!mapvote 2v2")
                    elif(int(pickupCount) == 3):
                        await ctx.send("!mapvote 3v3")
                    elif(int(pickupCount) == 4):
                        await ctx.send("!mapvote 4v4")
                    elif(int(pickupCount) == 5):
                        await ctx.send("!mapvote 5v5")
                    else:
                        await ctx.send("Could not determine format, please use !mapvote command")

                    await ctx.send("Your pickup is now ready, please put in your vote for the map and join the server at steam://connect/192.223.26.130:27015/janitor")
                    DePopulatePickup()
            else: 
                await ctx.send("You're already in this pickup vatos")
        
        elif(thxPickupActive == 1):
            player = ctx.author.display_name
            roles = ctx.author.roles
            if((player not in blueTeam) and (player not in redTeam)):
                    
                if("auto!" not in str(roles)):
                    print(pickupCount, player, len(redTeam))
                    if(len(redTeam) < int(pickupCount)):
                        redTeam.append(player)
                        
                elif(("auto!" in str(roles)) and ((len(blueTeam) < int(pickupCount)))):
                    blueTeam.append(player)

                bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                bEnumList = list(enumerate(blueTeam, start = 1))
                for i in range(len(bEnumList)):
                    bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│\n")
                bMsg = ''.join(bMsgList)

                rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                rEnumList = list(enumerate(redTeam, start = 1))
                for i in range(len(rEnumList)):
                    rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│\n")
                rMsg = ''.join(rMsgList)

                await ctx.send("Here are the teams!\n\n  **Team auto!**" + "```" + bMsg + "```\n\n\n**Team Outhouse**\n" +"```" + rMsg + "```")
                if ((len(blueTeam) == int(pickupCount)) and (len(redTeam) == int(pickupCount))):
                    
                    if(int(pickupCount) == 2):
                        await ctx.send("!mapvote 2v2")
                    elif(int(pickupCount) == 3):
                        await ctx.send("!mapvote 3v3")
                    elif(int(pickupCount) == 4):
                        await ctx.send("!mapvote 4v4")
                    elif(int(pickupCount) == 5):
                        await ctx.send("!mapvote 5v5")
                    else:
                        await ctx.send("Could not determine format, please use !mapvote command")

                    await ctx.send("Your pickup is now ready, please put in your vote for the map and join the server at steam://connect/192.223.26.130:27015/janitor")
                    DePopulatePickup()
            else: 
                await ctx.send("You're already in this pickup vatos")


'''@client.command(pass_context=True,)
@commands.has_role('Sanitation Engineers')
async def teams(ctx):
    global pickupLeader
    global pickupActive
    global rTotalPlayers
    global playerIDs
    
    if(ctx.message.channel.name == 'outhouse-pickups'):
        
        totalPlayers = list(rTotalPlayers)
        teamsPicked = 0
        totalPlayerSum = 0
        if(pickupActive == 1):
            if(len(rTotalPlayers) % 2 == 0):
                await ctx.send("Creating teams.. this may take a bit for larger games..")    
                teamCount = len(totalPlayers) / 2
                #combos = math.comb(len(totalPlayers), int(teamCount))
                combos = 1
                if(teamCount == 2):
                    combos = 70
                if(teamCount == 3):
                    combos = 70
                if(teamCount == 4):
                    combos = 252
                if(teamCount == 5):
                    combos = 252
                if(teamCount == 6):
                    combos = 924
                if(teamCount == 7):
                    combos = 3432
                if(teamCount == 8):
                    combos = 12870
                if(teamCount == 9):
                    combos = 48620
                    
                counter = 0
                if(teamCount >= 6):
                    counter = 2  
                print(teamCount)
                while(teamsPicked == 0):    
                    
                    for i in totalPlayers:
                        totalPlayerSum += int(rTotalPlayers[i])

                    for i in range(combos):  
                        nTotalPlayers = totalPlayers.copy()  
                        for i in range(int(teamCount)):
                            #print(nTotalPlayers)
                            print(counter)
                            playerPick = random.choice(nTotalPlayers)
                            blueTeam.append(playerPick)
                            nTotalPlayers.remove(playerPick)
                            
                        half = int(totalPlayerSum / 2)
                        blueRank = 0

                        for i in blueTeam:
                            blueRank += int(rTotalPlayers[i])

                        if((blueRank <= half + counter) and (blueRank >= half - counter)):
                            redTeam = nTotalPlayers.copy()
                            nTotalPlayers.clear()
                            teamsPicked = 1
                            break
                        else:
                            blueTeam.clear()
                            totalPlayerSum = 0
                    counter += 1
                    
                    

                bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                bEnumList = list(enumerate(blueTeam, start = 1))
                for i in range(len(bEnumList)):
                    bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│ \n")
                bMsg = ''.join(bMsgList)

                rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                rEnumList = list(enumerate(redTeam, start = 1))
                for i in range(len(rEnumList)):
                    rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│ \n")
                rMsg = ''.join(rMsgList)

                pickupActive = 0
                        
                await ctx.send("The game is ready to begin!\n\n  **Blue Team**" + "```" + bMsg + "```\n\n\n**Red Team**\n" +"```" + rMsg + "```")
                await ctx.send("Please react to the map you want to play on..")
                if((teamCount == 4)):
                    await ctx.send("!mapvote 4v4")
                elif((teamCount == 3) or (teamCount == 6)):
                    await ctx.send("!mapvote 3v3")
                elif(teamCount == 5):
                    await ctx.send("!mapvote 5v5")
                elif(teamCount == 7):
                    await ctx.send("!mapvote 7v7")
                elif(teamCount == 8):
                    await ctx.send("!mapvote 8v8")
                else:
                    await ctx.send("Can not determine the proper game format, please !mapvote yourself..")
                await ctx.send("You will be playing on this server - steam://connect/192.223.26.130:27015/janitor")
                print(playerIDs)

                

                for i in blueTeam:
                    user = client.get_user(playerIDs[i])
                    await user.send("Your pickup has started.  Please go back to The Outhouse and vote for your preferred map then join the server at steam://connect/192.223.26.130:27015/janitor")

                for i in redTeam:
                    user = client.get_user(playerIDs[i])
                    await user.send("Your pickup has started.  Please go back to The Outhouse and vote for your preferred map then join the server at steam://connect/192.223.26.130:27015/janitor")
                if(teamCount <= 4):
                    srv.execute("amx_cfg outhouse.cfg")
                elif(teamCount >= 5):
                    srv.execute("amx_cfg outhousefull.cfg")

                channel1  = client.get_channel(760160980738244628)
                await channel1.send("Red Team Rank Points: " + str(totalPlayerSum - blueRank))
                await channel1.send("Blue Team Rank Points: " + str(blueRank))
                await channel1.send("Estimated Rank Point Differential: " + str((counter - 1)))

            else:
                await ctx.send("You need an even number of players to start a pickup") 
        else:
            await ctx.send("There are no active pickups..")'''

@client.command(pass_context=True,)
@commands.has_role('Sanitation Engineers')
async def teams(ctx, gamemode = 'ctf'):
    global pickupLeader
    global pickupActive
    global rTotalPlayers
    global playerIDs
    global bVoiceList
    global rVoiceList

    if(ctx.message.channel.name == 'outhouse-pickups'):
        
        totalPlayers = list(rTotalPlayers)
        nTotalPlayers = totalPlayers.copy()
        random.shuffle(nTotalPlayers)
        teamsPicked = 0
        counter = 0
        totalPlayerSum = 0
        blueRank = 0
        redRank = 0
        blueTeam = []
        redTeam = []
        rEnumList = []
        if(pickupActive == 1):
            if(len(rTotalPlayers) % 2 == 0):
                await ctx.send("Creating teams.. this may take a bit for larger games..") 
                
                while(teamsPicked == 0): 
                    for i in totalPlayers:
                        totalPlayerSum += int(rTotalPlayers[i])      
                    teamCount = len(totalPlayers) / 2
                    combos = list(itertools.combinations(nTotalPlayers, int(teamCount)))
                    random.shuffle(combos)
                    for i in range(len(combos)):
                        redRank = 0
                        blueRank = 0
                        redTeam = nTotalPlayers.copy()
                        blueTeam = list(combos[i])
                        for i in blueTeam:
                            if i in redTeam:
                                redTeam.remove(i)
                                
                        half = int(totalPlayerSum / 2)
                        blueRank = 0

                        for i in blueTeam:
                            blueRank += int(rTotalPlayers[i])
                            bVoiceList.append(playerIDs[i])
                        for i in redTeam:
                            redRank += int(rTotalPlayers[i])
                            rVoiceList.append(playerIDs[i])
                        print(blueRank, half, counter)
                        if((blueRank <= half + counter) and (blueRank >= half - counter)):

                            nTotalPlayers.clear()
                            teamsPicked = 1
                            break
                        else:
                            blueTeam.clear()
                    totalPlayerSum = 0
                    counter += 1
                print(redTeam)
                print(blueTeam)   

                bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                bEnumList = list(enumerate(blueTeam, start = 1))
                for i in range(len(bEnumList)):
                    bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│ \n")
                bMsg = ''.join(bMsgList)

                rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                rEnumList = list(enumerate(redTeam, start = 1))
                for i in range(len(rEnumList)):
                    rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│ \n")
                rMsg = ''.join(rMsgList)

                pickupActive = 0
                        
                await ctx.send("The game is ready to begin!\n\n  **Blue Team**" + "```" + bMsg + "```\n\n\n**Red Team**\n" +"```" + rMsg + "```")
                await ctx.send("Please react to the map you want to play on..")
                if(gamemode.lower() == 'ctf'):    
                    if((teamCount == 2)):
                        await ctx.send("!mapvote 2v2")
                    if((teamCount == 4)):
                        await ctx.send("!mapvote 4v4")
                    elif(teamCount == 3):
                        await ctx.send("!mapvote 3v3")
                    elif(teamCount == 5):
                        await ctx.send("!mapvote 5v5")
                    elif(teamCount == 7):
                        await ctx.send("!mapvote 7v7")
                    elif(teamCount == 8):
                        await ctx.send("!mapvote 8v8")
                    elif(teamCount == 6):
                        await ctx.send("!mapvote 6v6")
                    else:
                        await ctx.send("Can not determine the proper game format, please !mapvote yourself..")
                    if((teamCount == 4) or (teamCount == 3)):
                        srv.execute("amx_cfg outhouse.cfg")
                    elif(teamCount >= 5):
                        srv.execute("amx_cfg outhousefull.cfg")
                    elif(teamCount >= 5):
                        srv.execute("amx_cfg 2v2.cfg")
                        srv.execute("outhousefull 0")
                elif(gamemode.lower() == 'adl'):
                    await ctx.send("!mapvote adl")
                    srv.execute("amx_cfg adl.cfg")
                
                await ctx.send("You will be playing on this server - steam://connect/192.223.26.130:27015/janitor")
                print(playerIDs)

                

                for i in blueTeam:
                    user = client.get_user(playerIDs[i])
                    await user.send("Your pickup has started.  Please go back to The Outhouse and vote for your preferred map then join the server at steam://connect/192.223.26.130:27015/janitor")

                for i in redTeam:
                    user = client.get_user(playerIDs[i])
                    await user.send("Your pickup has started.  Please go back to The Outhouse and vote for your preferred map then join the server at steam://connect/192.223.26.130:27015/janitor")
                

                channel1  = client.get_channel(760160980738244628)
                await channel1.send("Red Team Rank Points: " + str(redRank))
                await channel1.send("Blue Team Rank Points: " + str(blueRank))
                await channel1.send("Estimated Rank Point Differential: " + str((counter - 1)))

            else:
                await ctx.send("You need an even number of players to start a pickup") 
        else:
            await ctx.send("There are no active pickups..")

@client.command(pass_context=True)
async def players(ctx):
    pList = []
    for i in list(rTotalPlayers):
        pList.append(i + "   /   ")
    msg = ''.join(pList)

    await ctx.send(msg)

@client.command(pass_context=True,)
async def bw(ctx):
    await ctx.send("GET REKT BUCK")

@client.command(pass_context=True,)
async def concaim(ctx):
    await ctx.send("https://youtu.be/tVrJbiur_JU")

@client.command(pass_context=True,)
async def nox(ctx):
    await ctx.send("Just a reminder.. on 11/11/2020 at about 7:04 PST <@458068357376376844> killed <@264291540715700234> with a railgun on 2mesa3 during an intersquad scrimmage")

@client.command(pass_context=True,)
async def berg(ctx):
    await ctx.send("<@696886550201499768>")

@client.command(pass_context=True,)
async def statsme(ctx):
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name="statsME")
    await discord.Member.add_roles(member, role)
    await ctx.author.send("You have been assigned the 'statsME' role")

@client.command(pass_context=True)
@commands.has_role('Sanitation Engineers')
async def flush(ctx):
    if(ctx.message.channel.name == 'outhouse-pickups'):    
        if(pickupActive == 1) or (autoPickupActive == 1) or (thxPickupActive == 1):
            DePopulatePickup()
            await ctx.send("Pickup has been cancelled..")
        else:
            await ctx.send("There is no active pickup at this time..")



@client.command(pass_context=True)
async def remove(ctx):
    global pickupActive
    global playerIDs
    global rTotalPlayers
    global redTeam
    global blueTeam

    if(ctx.message.channel.name == 'outhouse-pickups'):    
        if(pickupActive == 1):    
            #playerID = ctx.author.id
            row = findPlayerRow(str(ctx.author.id))
            player = sheet.cell(row, 2).value

            del rTotalPlayers[player]
            #totalPlayers.remove(player)
            PopulateTable()
            await ctx.send("```" + msg + "```")
        elif(autoPickupActive == 1 or thxPickupActive == 1):
            if (ctx.author.display_name in blueTeam or ctx.author.display_name in redTeam):
                if(ctx.author.display_name in blueTeam):
                    blueTeam.remove(ctx.author.display_name)
                elif(ctx.author.display_name in redTeam):
                    redTeam.remove(ctx.author.display_name)
                
                bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                bEnumList = list(enumerate(blueTeam, start = 1))
                for i in range(len(bEnumList)):
                    bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│\n")
                bMsg = ''.join(bMsgList)

                rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                rEnumList = list(enumerate(redTeam, start = 1))
                for i in range(len(rEnumList)):
                    rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│\n")
                rMsg = ''.join(rMsgList)

                await ctx.send("Here are the teams!\n\n  **Team auto!**" + "```" + bMsg + "```\n\n\n**Team Outhouse**\n" +"```" + rMsg + "```")
                
            else:
                await ctx.send("You are not in this pickup..")


            
        else:
            await ctx.send("Currently there is no active pickup..")

@client.command(pass_context=True)
@commands.has_role('Sanitation Engineers')
async def voiceup(ctx):    
     
    # channel now holds the channel you want to move people into

    for i in bVoiceList:
        channel = client.get_channel(712749834603593748)
        member = ctx.guild.get_member(i)
        #member now holds the user that you want to move
        await member.move_to(channel)
    for i in rVoiceList:

        channel2 = client.get_channel(712749911996891137)
        member = ctx.guild.get_member(i)
        #member now holds the user that you want to move
        await member.move_to(channel2)

@client.command(pass_context=True)
async def test(ctx):    
    channel = client.get_channel(712749834603593748) 
    # channel now holds the channel you want to move people into

    member = ctx.guild.get_member(118900492607684614)
    #member now holds the user that you want to move

    await member.move_to(channel)

@client.command(pass_context=True)
async def halp(ctx):
    if(ctx.message.channel.name == 'outhouse-pickups'):    
        await ctx.send("```!pickup - Starts a pickup game\n"
                        + "!add - Adds you to the pickup game\n"
                        + "!remove - Removes you to the pickup game\n"
                        + "!teams - Randomly separates teams\n"
                        + "!flush - Cancels the pickup game\n"
                        + "!halp - Take a lucky guess...```")


#ON_MESSAGE EVENTS
@client.event
async def on_message(message):
    global pickupActive
    global totalPlayers
    global playerIDs
    global pickupCount
    global autoPickupActive
    global thxPickupActive
    global rTotalPlayers
    
    if(message.channel.name == 'outhouse-pickups'):    
        if((message.content.startswith("**Time's up! We have a winner!**")) or (message.content.startswith("**Right-o! We have a winner!**"))):
            wString = message.content
            wStringSplit = wString.split()
            uMap = wStringSplit[-1]
            nextMap = uMap[1:-1]

            srv.execute("amx_nextmap " + nextMap)
        if(message.content == "++"):
            with open('players.json') as f:
                playerRanks = json.load(f)
            playerID = message.author.id
            playerName = message.author.display_name   
            if(pickupActive == 1):   
                if(playerName not in list(rTotalPlayers)):    
                    if(str(playerID) not in list(playerRanks)):
                        insertHere = len(sheet.col_values(1)) + 1
                        #average = "=ROUNDDOWN(AVERAGEA(C" + str(insertHere) + ":G" + str(insertHere) + "))"
                        insertRow = [str(playerID), playerName, 5, 5, 5, 5, 5, 5]
                        sheet.insert_row(insertRow, insertHere)
                        playerRanks[playerID] = [playerName, 5, 5, 5, 5, 5]
                        channel = client.get_channel(760160980738244628)

                        with open('players.json', 'w') as fp:
                            json.dump(playerRanks, fp,indent= 4)
                        await channel.send(playerName + " with the player ID (" + str(playerID) + ") has been added to the rating list and needs a rating." )
                    
                    row = findPlayerRow(str(message.author.id))
                    playerName = sheet.cell(row, 2).value
                    playerRating = sheet.cell(row, 8).value
                    
                    playerIDs[playerName] = playerID
                    rTotalPlayers[playerName] = playerRating
                    PopulateTable()

                    await message.channel.send("```" + msg + "```")
                else:
                    await message.channel.send("You're already in the pickup vato..")

            elif(autoPickupActive == 1):
                player = message.author.display_name
                roles = message.author.roles
                if((player not in blueTeam) and (player not in redTeam)):
                        
                    if("auto!" not in str(roles)):
                        print(pickupCount, player, len(redTeam))
                        if(len(redTeam) < int(pickupCount)):
                            redTeam.append(player)
                            
                    elif(("auto!" in str(roles)) and ((len(blueTeam) < int(pickupCount)))):
                        blueTeam.append(player)

                    bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                    bEnumList = list(enumerate(blueTeam, start = 1))
                    for i in range(len(bEnumList)):
                        bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│\n")
                    bMsg = ''.join(bMsgList)

                    rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                    rEnumList = list(enumerate(redTeam, start = 1))
                    for i in range(len(rEnumList)):
                        rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│\n")
                    rMsg = ''.join(rMsgList)

                    await message.channel.send("Here are the teams!\n\n  **Team auto!**" + "```" + bMsg + "```\n\n\n**Team Outhouse**\n" +"```" + rMsg + "```")
                    if ((len(blueTeam) == int(pickupCount)) and (len(redTeam) == int(pickupCount))):
                        
                        if(int(pickupCount) == 2):
                            await message.channel.send("!mapvote 2v2")
                        elif(int(pickupCount) == 3):
                            await message.channel.send("!mapvote 3v3")
                        elif(int(pickupCount) == 4):
                            await message.channel.send("!mapvote 4v4")
                        elif(int(pickupCount) == 5):
                            await message.channel.send("!mapvote 5v5")
                        else:
                            await message.channel.send("Could not determine format, please use !mapvote command")

                        await message.channel.send("Your pickup is now ready, please put in your vote for the map and join the server at steam://connect/192.223.26.130:27015/janitor")
                        DePopulatePickup()
                else: 
                    await message.channel.send("You're already in this pickup vato")
                
            elif(thxPickupActive == 1):
                player = message.author.display_name
                roles = message.author.roles
                if((player not in blueTeam) and (player not in redTeam)):
                        
                    if("auto!" not in str(roles)):
                        print(pickupCount, player, len(redTeam))
                        if(len(redTeam) < int(pickupCount)):
                            redTeam.append(player)
                            
                    elif(("auto!" in str(roles)) and ((len(blueTeam) < int(pickupCount)))):
                        blueTeam.append(player)

                    bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                    bEnumList = list(enumerate(blueTeam, start = 1))
                    for i in range(len(bEnumList)):
                        bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│\n")
                    bMsg = ''.join(bMsgList)

                    rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                    rEnumList = list(enumerate(redTeam, start = 1))
                    for i in range(len(rEnumList)):
                        rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│\n")
                    rMsg = ''.join(rMsgList)

                    await message.channel.send("Here are the teams!\n\n  **Team auto!**" + "```" + bMsg + "```\n\n\n**Team Outhouse**\n" +"```" + rMsg + "```")
                    if ((len(blueTeam) == int(pickupCount)) and (len(redTeam) == int(pickupCount))):
                        
                        if(int(pickupCount) == 2):
                            await message.channel.send("!mapvote 2v2")
                        elif(int(pickupCount) == 3):
                            await message.channel.send("!mapvote 3v3")
                        elif(int(pickupCount) == 4):
                            await message.channel.send("!mapvote 4v4")
                        elif(int(pickupCount) == 5):
                            await message.channel.send("!mapvote 5v5")
                        else:
                            await message.channel.send("Could not determine format, please use !mapvote command")

                        await message.channel.send("Your pickup is now ready, please put in your vote for the map and join the server at steam://connect/192.223.26.130:27015/janitor")
                        DePopulatePickup()
                else: 
                    await message.channel.send("You're already in this pickup vato")
            else:
                await message.channel.send("No pickup active..")

        if(message.content == "--"):
            if(message.channel.name == 'outhouse-pickups'):       
                if(pickupActive == 1):    
                    playerID = message.author.id
                    row = findPlayerRow(str(playerID))
                    player = sheet.cell(row, 2).value

                    del rTotalPlayers[player]
                    #totalPlayers.remove(player)
                    PopulateTable()
                    await message.channel.send("```" + msg + "```")
                elif(autoPickupActive == 1 or thxPickupActive == 1):
                    if (message.author.display_name in blueTeam or message.author.display_name in redTeam):
                        if(message.author.display_name in blueTeam):
                            blueTeam.remove(message.author.display_name)
                        elif(message.author.display_name in redTeam):
                            redTeam.remove(message.author.display_name)
                        
                        bMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                        bEnumList = list(enumerate(blueTeam, start = 1))
                        for i in range(len(bEnumList)):
                            bMsgList.append("  " + str(bEnumList[i][0]) + " " * (3 - len(str(bEnumList[i][0]))) + "│ " + bEnumList[i][1] + (" " * (27 - len(bEnumList[i][1]))) + "│\n")
                        bMsg = ''.join(bMsgList)

                        rMsgList =  ['     │     Player Name            │\n', '-----╪----------------------------╪--\n']
                        rEnumList = list(enumerate(redTeam, start = 1))
                        for i in range(len(rEnumList)):
                            rMsgList.append("  " + str(rEnumList[i][0]) + " " * (3 - len(str(rEnumList[i][0]))) + "│ " + rEnumList[i][1] + (" " * (27 - len(rEnumList[i][1]))) + "│\n")
                        rMsg = ''.join(rMsgList)

                        await message.channel.send("Here are the teams!\n\n  **Team auto!**" + "```" + bMsg + "```\n\n\n**Team Outhouse**\n" +"```" + rMsg + "```")
                        
                    else:
                        await message.channel.send("You are not in this pickup..")
                else:
                    await message.channel.send("Currently there is no active pickup..")
            
        
    await client.process_commands(message)

print(len(sheet.col_values(1)))
client.run('NzU3MDgzNTkyNzM1MDY0MTY2.X2bPCg.QOndInrTzUQQMwNJF1BpSsnUarI')
