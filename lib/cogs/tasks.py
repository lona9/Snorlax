from discord.ext.commands import Cog
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import command
from datetime import datetime
from discord.ext import tasks
from datetime import timedelta
from discord.utils import get
from..db import db
import random
import pandas as pd

class Tasks(Cog):
  def __init__(self, bot):
    self.bot = bot

  @command(aliases=["t"])
  async def set_task(self, ctx, *args):
      tasktext = str(" ".join(args))

      taskid = datetime.now().strftime("%d/%m %%H%M%S")

      taskstatus = "pending"

      db.execute("INSERT OR IGNORE INTO tasks (TaskID, TaskText, TaskStatus) VALUES (?, ?, ?)", taskid, tasktext, taskstatus)

      db.commit()

      await ctx.send("Task added!")

  @command(aliases=["p", "pending"])
  async def check_pending(self, ctx):
      pending = "pending"
      pending_tasks = db.column("SELECT TaskText FROM tasks WHERE TaskStatus = ?", pending)
      print(pending_tasks)

      if pending_tasks == []:
          await ctx.send("There are no pending tasks.")
      else:
          for task in pending_tasks:
              taskmsg = await ctx.send(task)
              await taskmsg.add_reaction("✅")

  @command(aliases=["c", "completed"])
  async def check_done(self, ctx):
      done = "done"
      done_tasks = db.column("SELECT TaskText FROM tasks WHERE TaskStatus = ?", done)

      if done_tasks == []:
          await ctx.send("There are no completed tasks.")
      else:
          for task in done_tasks:
              taskmsg = await ctx.send(f"{task} :white_check_mark:")

  @command(aliases=["pc"])
  async def pending_clear(self, ctx):
      pending = "pending"
      db.execute("DELETE FROM tasks WHERE TaskStatus = ?", pending)
      db.commit()
      await ctx.send("Pending list cleared!")

  @command(aliases=["cc"])
  async def done_clear(self, ctx):
      done = "done"
      db.execute("DELETE FROM tasks WHERE TaskStatus = ?", done)
      db.commit()
      await ctx.send("Completed list cleared!")

  @Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.member.bot:
      pass

    else:
      if payload.emoji.name == "✅":
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        content = message.content

        done = "done"
        db.execute("UPDATE tasks SET TaskStatus = ? WHERE TaskText = ?", done, content)
        db.commit()

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("tasks")

def setup(bot):
  bot.add_cog(Tasks(bot))
