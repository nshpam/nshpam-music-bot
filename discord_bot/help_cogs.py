import discord
from discord.ext import commands

class help_cogs(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.channel = []
        self.title = "คู่มือการใช้งานแปม"
        self.help_message = """
        

    ℹ️   ?help: ดูคู่มือการใช้งาน
    ▶️ ?p <ชื่อเพลง>: สั่งให้แปมเล่นเพลงที่ค้นหา
    🔃 ?q : สั่งให้แปมแสดงคิวเพลงทั้งหมด
    ⏩ ?skip : สั่งให้แปมข้ามเพลงที่กำลังเล่นอยู่
    ⏸️ ?pause : สั่งให้แปมหยุดการเล่นเพลง
    ⏯️ ?resume : สั่งให้แปมเล่นเพลงที่หยุดต่อ
    🚮 ?clear : สั่งให้แปมลบเพลงทัั้งหมดในคิว
    👋 ?leave : เตะแปมออกจากช่องพูดคุย
    
        """
        self.embed1 = discord.Embed(
            title=self.title, 
            description=self.help_message, 
            color=0x76BA99)

    #CHECK IF THE BOT IS ONLINE
    '''@commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready')'''

    #BOT COMMANDS

    #SHOW HELP COMMAND
    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=self.embed1)
    
def setup(client):
    client.add_cog(help_cogs(client))