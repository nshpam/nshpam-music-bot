import discord
from discord.ext import commands

class test_vote(discord.Client):

    def __init__(self,client):
        self.client = client
        self.message = ''

    async def on_message(self, message):
        info = self.client.get_channel(988808176000442470)
        await info.send(message.content)