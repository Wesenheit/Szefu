from os import name
from sys import platform
import asyncio
from time import sleep
import discord
from discord import client
from discord.ext.commands.core import wrap_callback
from discord.team import Team
from discord.ext import commands,tasks
from ytd import *
from utils import *
from Queue import *
class Client:

    connected=False
    bot = commands.Bot(command_prefix='!',intents=discord.Intents().all())
    home='songs/'
    max_size_of_songs=1048576*1024
    queue=None

    @bot.command(name='join',help='dołącz do kanału')
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} nie połączony z żadnym kanałem głosowym".format(ctx.message.author.name))
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
        if len(temp)>0:
            await ctx.author.send(temp)
        else:
            await ctx.author.send("Nie ma obecnie żadnych piosenek zapisanych")

    @bot.command(name="kolejka",help="utwórz kolejkę")
    async def kolejka(ctx):
        if Client.queue==None:
            Client.queue=Queue()
            await ctx.send("Kolejka utworzona")
        else:
            await ctx.send("Kolejka już istnieje")
        
    @bot.command(name="dodaj",help="dodaj piosenkę do kolejki")
    async def dodaj(ctx,name):
        if Client.queue==None:
            await ctx.send("Kolejka nie istnieje")
        else:
            Client.queue.add(name)
    
    @bot.command(name="show",help="Pokaż kolejkę")
    async def show(ctx):
        if Client.queue==None:
            await ctx.send("Kolejka nie istnieje")
        else:
            await ctx.send(Client.queue.list())
    
    async def wrapper(ctx):
        await autocleanup(ctx,Client.max_size_of_songs)
        server = ctx.message.guild
        voice_channel = server.voice_client
        if Client.queue==None:
            await ctx.send("Kolejka nie istnieje")
            raise ValueError
        else:
            await Client.queue.updateplay(Client.bot.loop)
            if Client.queue.current==None:
                await ctx.send("Koniec kolejki")
                raise ValueError
            else:
                print(Client.queue.currname)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=Client.queue.currname))
                await ctx.send('**Leci teraz:** {}'.format(Client.queue.current))
                await Client.queue.downnex(Client.bot.loop)
                while True:
                    if voice_channel.is_playing():
                        await asyncio.sleep(2)
                    else:
                        await Client.wrapper(ctx)
    
    @bot.command(name="play_q",help="puść kolejkę")
    async def play_q(ctx):
        try:
            await Client.wrapper(ctx)
        except ValueError:
            pass


    @bot.command(name="dkolejka",help="usuń kolejkę")
    async def dkolejka(ctx):
        Client.queue=None
    
    @bot.command(name="remove",help='usuń n-ty element z kolejki')
    async def remove(ctx,n):
        if Client.queue==None:
            await ctx.send("Kolejka nie istnieje")
        else:
            Client.queue.remove(n)

    @bot.event
    async def on_message(message):
        if "czy można" in message.content:
            await message.channel.send(file=discord.File('bosak.jpg'))
        await Client.bot.process_commands(message)
    
    @bot.event
    async def on_member_update(before, after):
        game="League of Legends"
        if after.activity is not None:
            if game.lower() in after.activity.name.lower():
                await after.send("{}...\n nie graj proszę w {}".format(after.name,game))


    @bot.command(name="radio")
    async def play(ctx, url):
        if Client.connected:
            server = ctx.message.guild
            voice_channel = server.voice_client
            if voice_channel.is_playing():
                await ctx.send("Obecnie grany jest już utwór")
            else:
                try:
                    voice_channel.play(discord.FFmpegPCMAudio(str(url)))
                    await ctx.send('**radyjko**')
                except:
                    await ctx.send("Radio nieznalezione")
        else:
            await ctx.send("Bot niepołączony")

    def start(file):
        with open(file,"r") as f:
            name=f.readline()
        Client.bot.run(name)
        


