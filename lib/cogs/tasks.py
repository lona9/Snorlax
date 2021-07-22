from discord.ext.commands import Cog
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import command
from datetime import datetime
from discord.ext import tasks
from discord.utils import get
from..db import db

class Tasks(Cog):
  def __init__(self, bot):
    self.bot = bot

  @command(aliases=["t"])
  async def set_task(self, ctx, *args):
      tasktext = str(" ".join(args))

      taskid = datetime.now().strftime("%d/%m %H/%M/%S")

      taskstatus = "pending"

      await ctx.send("Please enter a category for this task:")

      try:
          message = await self.bot.wait_for('message', timeout=20, check=lambda message: message.author == ctx.author)

          category = str(message.content)

          db.execute("INSERT OR IGNORE INTO tasks (TaskID, TaskText, TaskStatus, TaskCategory) VALUES (?, ?, ?, ?)", taskid, tasktext, taskstatus, category)

          db.commit()

          await ctx.send(f"Task has been saved under the **{category}** category.")
      except:
          await ctx.send("Task has been saved with no category.")


  @command(aliases=["p", "pending"])
  async def check_pending(self, ctx):
      pending = "pending"
      categories = db.column("SELECT DISTINCT TaskCategory FROM tasks WHERE TaskStatus = ?", pending)

      if categories == []:
          await ctx.send("There are no pending tasks.")

      else:
                for category in categories:
                    await ctx.send(f"**{category} category**")
                    pending_tasks = db.column("SELECT TaskText FROM tasks WHERE TaskStatus = ? AND TaskCategory = ?", pending, category)

                    for task in pending_tasks:
                        taskmsg = await ctx.send(task)
                        await taskmsg.add_reaction("✅")
                        await taskmsg.add_reaction("🔃")


  @command(aliases=["c", "completed"])
  async def check_done(self, ctx):
      done = "done"
      categories = db.column("SELECT DISTINCT TaskCategory FROM tasks WHERE TaskStatus = ?", done)

      if categories == []:
          await ctx.send("There are no completed tasks.")
      else:
          for category in categories:
              await ctx.send(f"**{category} category**")

              done_tasks = db.column("SELECT TaskText FROM tasks WHERE TaskStatus = ? AND TaskCategory = ?", done, category)

              for task in done_tasks:
                  taskmsg = await ctx.send(task)

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

  @command()
  async def categories(self, ctx):
      categories = db.column("SELECT DISTINCT TaskCategory FROM tasks")

      categories = str(", ".join(categories))

      await ctx.send(f"These are your used categories for pending or done tasks currently on your lists: {categories}")

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

      elif payload.emoji.name == "🔃":
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        task_message = message.content

        await channel.send("Write a new category for this task:")

        try:
            new_category = await self.bot.wait_for('message', timeout=20, check=lambda message: message.author == payload.member)

            new_category = str(new_category.content)

            db.execute("UPDATE tasks SET TaskCategory = ? WHERE TaskText = ?", new_category, task_message)

            await channel.send(f"This task has now been saved under the **{category}** category.")

        except:
            await channel.send("Time's up! Nothing was changed.")

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("tasks")

def setup(bot):
  bot.add_cog(Tasks(bot))
