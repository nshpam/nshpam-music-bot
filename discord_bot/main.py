from calendar import c
import os
import discord
from discord.ext import commands

#IMPORT ALL COGS
from help_cogs import help_cogs
from music_cogs import music_cog
from vote_cogs import vote_cog
from test_vote import test_vote

TOKEN = 'OTg4NzkzMjU4OTYyNDYwNzEy.G0Adc-.1Ik6EDTsc_7-9Xgy7i5_oKyYOkSFMcyH7PnEvE'

client = commands.Bot(command_prefix = '?')
client.remove_command('help')

#SEND ONLINE MESSAGE
@client.event
async def on_ready():
    text_channel_list = [988808176000442470, 856901710009597972, 944191128972980265]

    '''
    988808176000442470   for_bot_only >>> NSHPAM's server
    856900883987562527   ห้องโสต >>> อนุบาลหมีควาย
    944191128972980265   song >>> Cpr.E but on 929 
    '''
    '''
    online_text = """
    👋 แปมพร้อมรับใช้ชาติ
    ➡️ดูวิธีใช้พิมพ์ ?help เลย⬅️
    """

    service_text = """
        🟩 เปิดเพลง 
        🟥 เปิดโหวต 
        🟥 สร้างนัดหมาย
        🟥 แจ้งเตือน 
        🟥 ถูพื้น
    """

    for channel in text_channel_list:
        info = client.get_channel(channel)
        embed = discord.Embed(
            title='🟩 ONLINE 🟩', 
            description=online_text, 
            color=0x76BA99)
        embed.add_field(name="Service", value=service_text, inline=False)

        await info.send(embed=embed)
    '''        
    print('Bot is online.')

#REGISTER COG
client.add_cog(help_cogs(client))
client.add_cog(music_cog(client))
client.add_cog(test_vote(client))
#client.add_cog(vote_cog(client))

client.run(TOKEN)
