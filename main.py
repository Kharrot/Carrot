import discord #the discord.py library
import asyncio #required to run async methods
import random #rng
import configparser #pulls credentials from auth.ini
import youtube_dl #music
import images #image module

config = configparser.ConfigParser()
config.read('auth.ini')
token = config.get('credentials', 'TOKEN')

bot = discord.Client()

@bot.event #startup
async def on_ready():
    print('Bot running')
    await bot.change_presence(game = discord.Game(name = '!help'))



@bot.event #commands
async def on_message(message):
#chat log
    if message:
        print(message.channel.name + ': ' + message.author.name + ': ' + message.content)

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
        await bot.send_message(message.channel, 'Right now the most viewed image on the imgur frontpage is: ' + images.topCommand().link)

#Shows a random image with the tag you mentioned
    elif message.content.lower().startswith('!img'):
        tag = message.content[5:]
        result = images.imgCommand(tag)
        if not result:
            await bot.send_message(message.channel, 'No images found for that tag :frowning:')
        else:
            await bot.send_message(message.channel, result.link)

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
