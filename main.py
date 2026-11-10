import asyncio
import os
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask
from python_aternos import Client

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_USER = os.getenv("ATERNOS_USER")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")

# --- Веб-сервер для Render (чтобы не было ошибки портов) ---
app = Flask("")


@app.route("/")
def home():
  return "Bot is running!"


def run_web():
  # Render автоматически передает порт через переменную окружения PORT
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


# --- Логика Discord бота ---
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


if __name__ == "__main__":
  # Запускаем веб-сервер в отдельном потоке
  t = Thread(target=run_web)
  t.start()

  # Запускаем Discord-бота
  if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
  else:
    print("❌ Ошибка: Не найден DISCORD_TOKEN в переменных окружения!")
