from os import name
import discord
from discord import client
from discord.team import Team
from discord.ext import commands,tasks
from ytd import *
from utils import *

class Client:

    connected=False
    bot = commands.Bot(command_prefix='!')
    home='songs/'
    max_size_of_songs=100000000000000000
    
    @bot.command(name='join',help='dołącz do kanału')
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} nie połączony z rzadnym kanałem głosowym".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
            Client.connected=True
            await channel.connect()
    
    @bot.command(name='leave', help='Opuść kanał')
    async def leave(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            Client.connected=False
            await voice_client.disconnect()
        else:
            await ctx.send("Bot niepołączony")

    @bot.command(name='play_mp3',help="puść plik mp3")
    async def play_mp3(ctx,name):
        if Client.connected:
            server = ctx.message.guild
            voice_channel = server.voice_client
            try:
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=Client.home+name+".mp3"))
                await ctx.send('**Leci teraz:** {}'.format(name))
            except:
                await ctx.send("Utwór nieznaleziony")
        else:
            await ctx.send("Bot niepołączony")

    @bot.command(name='replay',help="puść plik mp3")
    async def replay(ctx,name):
        if Client.connected:
            server = ctx.message.guild
            voice_channel = server.voice_client
            try:
                if name in list():
                    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=name))
                    await ctx.send('**Leci teraz:** {}'.format(name))
                else:
                    await ctx.send("Utwór nieznaleziony")
            except:
                await ctx.send("Utwór nieznaleziony")
        else:
            await ctx.send("Bot niepołączony")

    @bot.command(name='play_yt',help="puść plik mp3")
    async def play_yt(ctx,name):
        await autocleanup(ctx,Client.max_size_of_songs)
        if Client.connected:
            server = ctx.message.guild
            voice_channel = server.voice_client
            if voice_channel.is_playing():
                await ctx.send("Obecnie grany jest już utwór")
            else:
                try:
                    filename = await YTDLSource.from_url(name, loop=Client.bot.loop)
                    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
                    await ctx.send('**Leci teraz:** {}'.format(name))
                except:
                    await ctx.send("Utwór nieznaleziony")
        else:
            await ctx.send("Bot niepołączony")

    @bot.command(name='pause', help='zapauzuj piosenkę')
    async def pause(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("obecnie nie jest grany żaden utwór")

    @bot.command(name='resume', help='kontynuuj piosenkę')
    async def resume(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("Nic nie jest obecnie grane")
    @bot.command(name='stop', help='zatrzymaj piosenkę')
    async def stop(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await ctx.send("obecnie nie jest grany żaden utwór")

    @bot.command(name="size",help='zwraca rozmiar plików')
    async def size(ctx):
        await ctx.send("Obecnie zajmowana przestrzeń to {}".format(size()))

    @bot.command(name='cleanup',help="usuń pobrane piosenki")
    async def clean(ctx):
        cleanup()
        await ctx.send("Usunięto zapisane piosenki")

    @bot.command(name='list',help='Pokazuje zapisane piosenki')
    async def lista(ctx):
        temp=''
        for a in list():
            temp+=a+'\n'
            if len(temp)>2000:
                temp=temp[:-len(a)]
                await ctx.author.send(temp)
                temp=a
        await ctx.author.send(temp)
            
    def start(file):
        with open(file,"r") as f:
            name=f.readline()
        Client.bot.run(name)
        


