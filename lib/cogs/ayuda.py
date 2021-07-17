import discord
import os
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed

class Ayuda(Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.remove_command("help")

  @command()
  async def help(self, ctx):

    self.ctx = ctx

    embed = Embed()

    fields = [("Hi!", "I'm Snorlax, and I'll be your personal assistant from now on! Read the commands below to know how to interact with me.", False),
                ("You can use the following commands for tasks:", "**!task (or !t)**: use this command to add a task to your list of pending tasks.\n**!pending (or !p)**: get the list of pending tasks, and move them to the done list, reacting to the message.\n**!completed (or !c)**: get the list of completed tasks.\n**!pc**: or *pending clear*, clears your entire pending list.\n**!cc**: or *completed clear*, clears your entire completed list.", False),
                ("You can use the following command for reminders:", "**!reminder (or !r)**: type the command and the time you want the reminder to be sent and your message. input takes seconds (s), minutes (m), hours (h) and days (d) with a whole number, and just one at a time, for example: *!r 2h reply to emails* or *!r 1d kristen's birthday*. You will receive the reminder in the same channel you sent the command.", False)]

    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)

    embed.set_author(name='snorlax', icon_url="https://cdn.discordapp.com/attachments/804445064029798431/865762593955512350/imagen_2021-07-16_211126.png")

    await ctx.channel.send(embed=embed)


  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("ayuda")

def setup(bot):
  bot.add_cog(Ayuda(bot))
