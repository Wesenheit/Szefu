from os import name
import discord
from discord import client
from discord.team import Team
from discord.ext import commands,tasks

class Client:

    connected=False
    bot = commands.Bot(command_prefix='!')
    home='songs/'

    @bot.command(name='join',help='dołącz do kanału')
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} sdasdasd".format(ctx.message.author.name))
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


    @bot.command(name='pause', help='zapauzuj piosenkę')
    async def pause(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("obecnie nie jest grany żaden utwór")

    @bot.command(name='resume', help='kontynuuj piosenkę')
    async def resume(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("")
    @bot.command(name='stop', help='zatrzymaj piosenkę')
    async def stop(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("obecnie nie jest grany żaden utwór")


    def start(file):
        with open(file,"r") as f:
            name=f.readline()
        Client.bot.run(name)
        


