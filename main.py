import asyncio
import os
import discord
from discord.ext import commands
from python_aternos import Client

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_USER = os.getenv("ATERNOS_USER")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"✅ Бот {bot.user} успешно запущен и готов к работе!")


@bot.command(name="start")
async def start_server(ctx):
  await ctx.send("⏳ Отправляю запрос на запуск сервера Aternos...")
  try:
    # Исправленный способ авторизации через Client
    aternos = Client()
    aternos.login(ATERNOS_USER, ATERNOS_PASSWORD)
    servs = aternos.list_servers()
    myserver = servs[0]

    myserver.start()
    await ctx.send(
        "🚀 Сервер **Ruslanis13** запускается! Ожидайте 1-3 минуты."
    )
  except Exception as e:
    await ctx.send(f"❌ Ошибка при запуске: {e}")


@bot.command(name="status")
async def server_status(ctx):
  try:
    aternos = Client()
    aternos.login(ATERNOS_USER, ATERNOS_PASSWORD)
    servs = aternos.list_servers()
    myserver = servs[0]

    status = myserver.status
    await ctx.send(f"📊 Текущий статус сервера: **{status}**")
  except Exception as e:
    await ctx.send(f"❌ Не удалось получить статус: {e}")


if DISCORD_TOKEN:
  bot.run(DISCORD_TOKEN)
else:
  print("❌ Ошибка: Не найден DISCORD_TOKEN в переменных окружения!")
