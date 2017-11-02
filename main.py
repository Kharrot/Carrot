import discord
import asyncio
import random
import configparser
import youtube_dl
from imgurpython import ImgurClient

config = configparser.ConfigParser()
config.read('auth.ini')
client_id = config.get('credentials', 'client_id')
client_secret = config.get('credentials', 'client_secret')
token = config.get('credentials', 'TOKEN')

client = ImgurClient(client_id, client_secret)

bot = discord.Client()



@bot.event #startup
async def on_ready():
    print('Bot running')
    await bot.change_presence(game = discord.Game(name = '!help'))



@bot.event #commands
async def on_message(message):

#help command
    if message.content.lower().startswith('!help'):
        helpCommand = ('**__Commands__**\n\n'
                       '___Image(Imgur) commands___:\n'
                       '!top  --> Shows the top viewed image on the imgur frontpage\n'
                       '!img [tag]  --> Shows a random image with that tag')
        await bot.send_message(message.channel, helpCommand)

# ----------------------- IMAGE COMMANDS ------------------------------
#Shows the top viewed image on the imgur frontpage
    elif message.content.lower().startswith('!top'):
        items = client.gallery()
        max_item = None
        max_views = 0
        for item in items:
            if item.views > max_views:
                max_item = item
                max_views = item.views
        await bot.send_message(message.channel, 'Right now the most viewed image on the imgur frontpage(' + str(max_views) + ' views) is: ' + max_item.link)


#Shows a random image with the tag you mentioned
    elif message.content.lower().startswith('!img'):
        tag = message.content[5:]
        items = client.gallery_search(tag)
        if not items:
            await bot.send_message(message.channel, 'No images found for that tag :frowning:')
        else:
            resultimg = random.choice(items)
            await bot.send_message(message.channel, resultimg.link)

#---------------------------------- MUSIC COMMANDS ---------------------------------
#Lets the bot leave voice
    elif message.content.lower().startswith('!quit'):
        voice_client = bot.voice_client_in(message.server)
        if not voice_client:
            await bot.send_message(message.channel, 'I\'m not in a voice channel right now')
        else:
            await voice_client.disconnect()

#Lets the bot join your voice channel and plays a song
    elif message.content.lower().startswith('!play'):
        channel = message.author.voice.voice_channel
        if not channel:
            await bot.send_message(message.channel, 'You have to be in a voice channel')
        else:
            voice_client = bot.voice_client_in(message.server)
            if not voice_client:
                voice = await bot.join_voice_channel(channel)
                yt_url = message.content[6:]
                if not yt_url:
                    await bot.send_message(message.channel, 'You have to provide a link to a youtube video')
                else:
                    player = await voice.create_ytdl_player(yt_url)
                    player.start()
            else:
                await voice_client.disconnect()
                voice = await bot.join_voice_channel(channel)
                yt_url = message.content[6:]
                if not yt_url:
                    await bot.send_message(message.channel, 'You have to provide a link to a youtube video')
                else:
                    player = await voice.create_ytdl_player(yt_url)
                    player.start()


bot.run(token)
