import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
        #all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None
        self.embed = ''
        self.title = ''
        self.thumbnail = ''

      #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        self.thumbnail = info.get('thumbnail')
        self.title = info['title']
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    
        else:
            self.is_playing = False
    
    # infinite loop checking 
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    self.embed = discord.Embed(
                        title='💿 Now playing 💿', 
                        description="❌ แปมไม่สามารถเข้าไปเล่นเพลงได้ ❌", 
                        color=0x76BA99)
                    await ctx.send(embed=self.embed)
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            self.embed = discord.Embed(
                        title='💿 Now playing 💿', 
                        description="%s" %self.title, 
                        color=0x76BA99)
            await ctx.send(embed=self.embed)
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            self.embed = discord.Embed(
                        title='💿 Please join the channel 💿', 
                        description="❌ แปมไม่รู้ว่าควรเข้าห้องไหน ❌", 
                        color=0x76BA99)
            await ctx.send(embed=self.embed)
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                self.embed = discord.Embed(
                        title='💿 Now playing 💿', 
                        description="❌ แปมไม่สามารถเปิดเพลงได้ ❌", 
                        color=0x76BA99)
                await ctx.send(embed=self.embed)
            else:
                self.embed = discord.Embed(
                    title='💿 Added Track 💿', 
                    description="➡️ เพิ่ม %s เข้าในคิว" %self.title, 
                    color=0x76BA99)
                self.embed.set_image(url=self.thumbnail)
                await ctx.send(embed=self.embed)
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            self.embed = discord.Embed(
                        title='💿 Paused Track 💿', 
                        description="⏹️ แปมหยุดเล่น %s" %self.title, 
                        color=0x76BA99)
            self.embed.set_image(url=self.thumbnail)
            await ctx.send(embed=self.embed)
        elif self.is_paused:
            self.vc.resume()

    @commands.command(name = "resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.vc.resume()
            self.embed = discord.Embed(
                        title='💿 Now playing 💿', 
                        description="⏯️ แปมเล่น %s" %self.title, 
                        color=0x76BA99)
            self.embed.set_image(url=self.thumbnail)
            await ctx.send(embed=self.embed)

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)
            self.embed = discord.Embed(
                        title='💿 Skipped Track 💿', 
                        description="⏩ แปมข้าม %s " %self.title, 
                        color=0x76BA99)
            self.embed.set_image(url=self.thumbnail)
            await ctx.send(embed=self.embed)


    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        self.embed = discord.Embed(
                        title='💿 Track Queue 💿', 
                        description="🎵🎵🎵 คิวเพลง 🎵🎵🎵", 
                        color=0x76BA99)
        await ctx.send(embed=self.embed)
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += str(i+1)+ ". " + self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            self.embed = discord.Embed(
                        title='💿 Track Queue 💿', 
                        description="❌❌❌ ไม่มีเพลงอยู่ในคิว ❌❌❌", 
                        color=0x76BA99)
            await ctx.send(embed=self.embed)

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        self.embed = discord.Embed(
                        title='💿 Cleared Queue 💿', 
                        description="❗❗❗ แปมล้างเพลงทั้งหมดในเพลย์ลิสต์ ❗❗❗", 
                        color=0x76BA99)
        await ctx.send(embed=self.embed)

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        self.embed = discord.Embed(
                        title='👋 Goodbye 👋', 
                        description="😭😭😭 แปมหมดประโยชน์แล้วสินะ 😭😭😭", 
                        color=0x76BA99)
        await ctx.send(embed=self.embed)
        await self.vc.disconnect()
        
        
