import discord
import asyncio
import re
import datetime
import math

# A pattern to match the word vore, and only the single word vore.
pattern = re.compile(r'\b[V|v][O|o][R|r][E|e]\b')
serverAndDate = {}
botStartup = datetime.datetime.now()
lastMention = datetime.datetime.now() - datetime.timedelta(days=1)


client = discord.Client()

def readTimesFromFile():
    global serverAndDate
    with open("timeStamps.txt", "r") as target:
        for line in target:
            tmp = line.split(',')
            tmp[1] = tmp[1][0:-1]
            serverAndDate[tmp[0]] = datetime.datetime.strptime(tmp[1], "%Y-%m-%d %H:%M:%S")
            

def writeTimesToFile():
    with open('timeStamps.txt', 'w') as target:
        for serverId in serverAndDate:
            target.write('{},{}\n'.format(serverId, serverAndDate[serverId].strftime("%Y-%m-%d %H:%M:%S")))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    readTimesFromFile()
    print('Stored server info:')
    for id in serverAndDate:
        print ("id: {}, time: {}".format(id, serverAndDate[id]))

@client.event
async def on_message(message):
    global botStartup
    global serverAndDate
    currentTime = datetime.datetime.now()
    
    bot = None
    for x in message.server.members:
        if client.user.id == x.id:
            bot = x
            break

    # Timezone hack, apparently isn't needed for Heroku.
    lastReferenced = bot.joined_at #- datetime.timedelta(hours=4)
    if message.server.id in serverAndDate:
        lastReferenced = serverAndDate[message.server.id]

    # Begin time formatting
    diff = currentTime - lastReferenced
    hours = math.floor(diff.seconds/3600)
    minutes = math.floor((diff.seconds - hours * 3600)/60)
    seconds = diff.seconds - hours * 3600 - minutes * 60
    dt = "{} days, ".format(diff.days)
    ht = "{} hours, ".format(hours)
    mt = "{} minutes, and ".format(minutes)
    st = "{} seconds".format(seconds)

    if diff.days == 1:
        dt = "1 day, "
    elif diff.days == 0:
        dt = ""
        if hours == 0:
            ht = ""
            mt = "{} minutes and ".format(minutes)
            if minutes == 0:
                mt = ""

    if hours == 1:
        ht = "1 hour, "
    if minutes == 1:
        if ht == "":
            mt = "1 minute and"
        else:
            mt = "1 minute, and "
    if seconds == 1:
        st = "1 second"
    # End Time formatting stuff


    if message.content.startswith('!vt'):
        await client.send_message(message.channel, 'The server has gone {}{}{}{} without mentioning vore (aside from these messages).'.format(dt, ht, mt, st))
    elif ((pattern.search(message.content) is not None) and (message.author.id != client.user.id)):
        serverAndDate[message.server.id] = currentTime
        writeTimesToFile()
        #if ((currentTime - lastMention).total_seconds() >= 900):
        await client.send_message(message.channel, '{} referenced vore, setting the counter back to 0.\n The server went {}{}{}{} without mentioning vore.'.format(message.author.mention, dt, ht, mt, st))
        lastMention = currentTime

client.run('MzU1MTQ0NDUwNDM3MDIxNjk3.DJIlnQ.Yg56nQ6JdLbxUDmlkFnuu6ay2FM')