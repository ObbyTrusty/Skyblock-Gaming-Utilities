import os
import sqlite3
import aiohttp
from discord.ext import commands, tasks


class GuildTasks(commands.Cog):
    def __init__(self, bot):
        if os.getenv("DEBUGMODE") != "True":
            self.guildvoicemembercount.start()
        self.bot = bot

    def cog_unload(self):
        self.guildvoicemembercount.cancel()

    @tasks.loop(hours=6)
    async def guildvoicemembercount(self):
        await self.bot.wait_until_ready()
        try:
            conn = sqlite3.connect('database/SGGuildDB.sqlite')
            c = conn.cursor()
            c.execute(f'''SELECT * FROM sgguildutilsdb''')
            guilds = c.fetchall()
        except Exception as e:
            print(e)
        try:
            tempcheck = guilds
        except Exception as e:
            print(e)
            return
        for guild in guilds:
            try:
                if guild[2] is None:
                    break
                else:
                    pass
                discordid = guild[0]
                guildid = guild[1]
                voiceid = guild[2]
                guild = self.bot.get_guild(discordid)
                print(guild)
                guildvoicechannel = guild.get_channel(voiceid)
                session = aiohttp.ClientSession()
                response = await session.get(f'https://api.hypixel.net/guild?key={os.getenv("APIKEY")}&id={guildid}')
                if response.status != 200:
                    return
                data = await response.json()
                if data['success'] == False:
                    return
                if data['guild'] is None:
                    return
                await guildvoicechannel.edit(
                    name=f'{data["guild"]["name"]} Members: {len(data["guild"]["members"])}')
                print(f'Updated Voice for {guild}')
                await session.close()
            except Exception as e:
                print(e)


def setup(bot):
    bot.add_cog(GuildTasks(bot))
