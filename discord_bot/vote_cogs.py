import discord
from discord.ext import commands
import datetime

class vote_cog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embed = ''
        self.temp = ''
        self.vote_manual = """

    ℹ️   คู่มือการใช้งานบอทโหวต ℹ️
     👀 ?show หัวข้อ : โหวตแบบแสดงชื่อ
        💡ตัวอย่าง ?1 coffee or tea

     💀 ?hide หัวข้อ : โหวตแบบนิรนาม
        💡ตัวอย่าง ?2 ชอบหมาหรือแมว

     📌 ?result (CODE): แสดงผลโหวต ณ ตอนนี้
        💡ตัวอย่าง ?result 0001
        """
        #SET TIME
        self.time_now = datetime.datetime.now()
        self.start = self.time_now.strftime("%d %B %Y %X")
        self.end = False

        self.mode = ''
        self.info = """
        📌 กด 👍 👎 เพื่อโหวต
        🟩 MODE %s 
        """ %(self.mode)


    @commands.command()
    async def vote(self,ctx):
        await ctx.send(self.vote_manual)

    #SHOW VOTERS
    @commands.command()
    async def create_poll(self,ctx,mode=None,query=None):
        #QUERY OPTIONS

        if query == None:
            self.embed = discord.Embed(
                            title='❌❌❌ ไม่สามารถเปิดโหวตได้ ❌❌❌', 
                            description="กรุณาใสหัวข้อที่จะโหวต ❗", 
                            color=0x76BA99)
        else:
            self.mode = '👀 โหวตแบบแสดงชื่อ'
                #จะเอา message จากช่องข้อความมายังไง
                #อย่าลืมทำระบบส่งข้อความเมื่อบอท offline
            self.embed = discord.Embed(
                            title='🟩 %s' %query, 
                            description=self.info, 
                            color=0x76BA99)
            self.embed.add_field(name="START", value=self.start, inline=False)
        await ctx.send(embed=self.embed)
