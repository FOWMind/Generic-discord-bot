'''
********************************************************************************
    Generic Discord bot
        Check out the documentation:
            https://github.com/Rapptz/discord.py
            https://discordpy.readthedocs.io/en/latest/
        Here some examples:
            https://github.com/Rapptz/discord.py/tree/master/examples

    Remember to use pipenv
********************************************************************************
'''



# Import DiscordPy
import discord
from discord.ext import commands

import datetime
from urllib import parse, request

# RegExs
import re

from random import randint


# Custom functions
def command_fail(name: str):
    # Message for console debugging
    print( 'An error ocurred while executing "{}" function.\n'.format(name) )


def getRandomFromList(li):
    try:
        rand_number = randint( 0, len(li) )
        # Pick a random index from a list
        result = str(li[rand_number])
        
        return result
    except:
        command_fail('getRandomFromList')








# You can use !, -, ?, ¿, botName+Sign, etc.
bot_prefix = 'myBot!' # myBot!command parameters

bot = commands.Bot(command_prefix=bot_prefix, description='Here a description of your bot')

''' Events '''
@bot.event
async def on_ready():
    print('I\'m connected.')
    # await bot.change_presence( activity=discord.Streaming(name='Streamear Name', url='https://twitch.tv/StreamerName') )
    await bot.change_presence( activity=discord.Game(name="Game you want") )




# {} = user mention
welcome_list = ['Welcome, {}', 'Hi, {}, welcome to our server.', 'Hey, {}. welcome.']

# must be <int> type
welcome_channel_id = 1234567890

@bot.event
async def on_member_join(member):
    try:
        welcome_channel = bot.get_channel(welcome_channel_id)
        await welcome_channel.send( getRandomFromList(welcome_list).format(member.mention) )
    except:
        print( 'Cannot sent message to {}. Please verify welcome_channel'.format(member.name) )





''' Commands '''
@bot.command()
async def ping(ctx):
    # test your bot on Discord with this command
    await ctx.send('pong')

# General
@bot.command()
async def sum(ctx, *numbers):
    try:
        total = 0

        for num in numbers:
          total += float(num)
        await ctx.send(total)
    except:
        command_fail('sum')

discordIconURL = 'https://cdn.discordapp.com/icons/'
@bot.command()
async def info(ctx):
    try:
        # ctx.guild is your server
        embed = discord.Embed(
            title=f"{ctx.guild.name}",
            description="Server info: ",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Creation date: ", value=f"{ctx.guild.created_at}")
        embed.add_field(name="Owner: ", value=f"{ctx.guild.owner}")
        embed.add_field(name="Region: ", value=f"{ctx.guild.region}")
        embed.add_field(name="ID: ", value=f"{ctx.guild.id}")

        # Select your server icon and put it like a thumbnail
        embed.set_thumbnail( url='{}{}/{}'.format(discordIconURL, ctx.guild.id, ctx.guild.icon) )

        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("I can't send you this information. :(")


# Messages
@bot.command()
async def gg(ctx):
    try:
        await ctx.send('GG WP!')
    except:
        command_fail('gg')


@bot.command()
async def say(ctx, *, message: str):
    try:
        await ctx.send(message)
    except:
        command_fail('say')



quotes = ['Simple quote', 'Quote two', 'Quote three']

@bot.command()
async def quote(ctx):
    try:
        await ctx.send( getRandomFromList(quotes) )
    except:
        command_fail('quote')



# Gif commands
def getGif(search):
    # needs object
    query = parse.urlencode( {'search': search} )
    query = query.replace('=', '/')

    # https://tenor.com/search/userQuery
    html = request.urlopen( 'https://tenor.com/{}'.format(query) ).read().decode()

    # Get gif hash with RegEx from an HTML text (decoded by decode() method)
    results = re.findall(r"images/(\S{32})", html)

    return results





def shortGif(author, feel, to = ''):
    gifs = getGif(feel)
    getGifLen = len(gifs)

    gifUrl = 'https://media.tenor.com/images/{}/tenor.gif'.format( gifs[randint(0, getGifLen)] )


    # you can use a RegEx to detect a user mention ('<!@userId>')
    if to == str(to) and '@' in to:

        # first {} = message author, second {} = user to whom it is sent
        switch = {
            'angry': '**{}** is angry with **{}**',
            'sad': '**{}** feels sad for **{}**. :(',
            'happy': '**{}** is happy for **{}**.',
            'weird': '**{}** send weird gif to **{}**',
            'hug': '¡**{}** hugs **{}**!',
            'kiss': '¡**{}** kissed **{}**!',
            'kick': '**{}** kick **{}**. >:('
        }

        # This is equivalent to: switch { case 'angry': value = ... }
        feelMessage = switch.get(str(feel), '').format(author, to)
    else:
        # if author doesn't select a destinatary
        switch = {
            'angry': '**{}** feels angry.',
            'sad': '**{}** feels sad. :(',
            'happy': '**{}** is happy.',
            'confused': 'Hmm, **{}** is confused.',
            'weird': '**{}** says something is weird.',
            'hug': '¡**{}** hugs you!',
            'kiss': '¡**{}** is kissing you!',
            'kick': '**{}** kicked you. >:(',
            'shoot': '**{}** shoot you.'
        }
    
        feelMessage = switch.get(str(feel), '').format(author)

    embed = discord.Embed(description=f"{feelMessage}", color=discord.Color.blue())
    embed.set_image(url=gifUrl)

    return embed


@bot.command()
async def sad(ctx, to = ''):
    try:
        emb = shortGif(ctx.author.name, 'sad', to)
        await ctx.send(embed=emb)
    except:
        command_fail('sad')

@bot.command()
async def angry(ctx, to = ''):
    try:
        emb = shortGif(ctx.author.name, 'angry', to)
        await ctx.send(embed=emb)
    except:
        command_fail('angry')

@bot.command()
async def happy(ctx, to = ''):
    try:
        emb = shortGif(ctx.author.name, 'happy', to)
        await ctx.send(embed=emb)
    except:
        command_fail('happy')

@bot.command()
async def confused(ctx):
    try:
        emb = shortGif(ctx.author.name, 'confused')
        await ctx.send(embed=emb)
    except:
        command_fail('confused')

@bot.command()
async def weird(ctx, to = ''):
    try:
        emb = shortGif(ctx.author.name, 'weird', to)
        await ctx.send(embed=emb)
    except:
        command_fail('weird')

@bot.command()
async def hug(ctx, to = ''):
    try:
        emb = shortGif(ctx.author.name, 'hug', to)
        await ctx.send(embed=emb)
    except:
        command_fail('hug')

@bot.command()
async def kiss(ctx, to = ''):
    try:
        emb = shortGif(ctx.author.name, 'kiss', to)
        await ctx.send(embed=emb)
    except:
        command_fail('kiss')

@bot.command()
async def kick(ctx, to = ''):
    try:
        emb = shortGif(ctx.author.name, 'kick', to)
        await ctx.send(embed=emb)
    except:
        command_fail('kick')

@bot.command()
async def shoot(ctx, to = ''):
    try:
        emb = shortGif(ctx.author.name, 'shoot', to)
        await ctx.send(embed=emb)
    except:
        command_fail('shoot')








# Youtube commands
def getYoutubeVideo(search):
    query = parse.urlencode( {'search_query': search} )

    # http://www.youtube.com/results?search_query=userQuery
    html = request.urlopen( 'http://www.youtube.com/results?{}'.format(query).read().decode() )
    
    # Get youtube links with RegEx from an HTML text (decoded by decode() method)
    results = re.findall(r"watch\?v=(\S{11})", html)
    
    return results


@bot.command()
async def youtube(ctx, *, search):
    try:
        # send first video found to chat
        await ctx.send( 'https://www.youtube.com/watch?v={}'.format( getYoutubeVideo(search)[0] ) )
    except:
        command_fail('youtube')

@bot.command()
async def ytlist(ctx, *, search):
    try:
        results_len = len( getYoutubeVideo(search) )
        
        # For each youtube video its can found, send a message (max 5)
        for i in range(0, results_len):
            if i == 5:
                break
            await ctx.send( 'https://www.youtube.com/watch?v={}'.format( getYoutubeVideo(search)[i] ) )
            i += 1
    except:
        command_fail('ytlist')






# Loop command
@bot.command()
async def repeat(ctx, times, *, string):
    try:
        times = int(times)
        maxRepeats = 30
        maxDigits = 100
        if (times <= maxRepeats and len(string) <= maxDigits):
            i = 0
            message = ''
            while i <= times:
                message += string + ' '
                i += 1
        else:
            errorMessage = '''> You can only repeat {} times maximum!\n
            Make sure you have less than {} characters in the text that you want to repeat.'''.format(maxRepeats, maxDigits)

            await ctx.send(errorMessage, delete_after=7.0)
            return
            
        if len(message) > 0:
            await ctx.send(message)
    except:
        command_fail('repeat')



botToken = 'YOUR KEY'
bot.run(botToken)