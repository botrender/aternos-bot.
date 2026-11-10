import os
import threading
from flask import Flask
from discord.ext import commands
import discord
from pythonaternos import Client

# --- НАСТРОЙКА FLASK ДЛЯ RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Aternos Discord Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

# --- НАСТРОЙКА DISCORD БОТА ---
intents = discord.Intents.default()
intents.message_content = True  # Обязательно для чтения команд!

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Бот авторизован в Discord как {bot.user}')

@bot.command(name='status')
async def status(ctx):
    await ctx.send("Проверяю статус сервера...")
    try:
        session_cookie = os.getenv("ATERNOS_SESSION")
        if not session_cookie:
            await ctx.send("Ошибка: Не задана переменная ATERNOS_SESSION в Render!")
            return

        # Авторизация по куки для обхода Cloudflare
        aternos = Client.from_minicookie(session_cookie)
        servers = aternos.list_servers()
        
        if not servers:
            await ctx.send("Не найдено ни одного сервера Aternos в этом аккаунте.")
            return

        server = servers[0] # Берем первый сервер из списка
        
        # Переводим статус на русский для удобства
        status_text = {
            'online': '🟢 Онлайн',
            'offline': '🔴 Оффлайн',
            'loading': '🟡 Запускается...',
            'queuing': '⏳ В очереди...'
        }.get(server.status, server.status)

        await ctx.send(f"**Сервер:** {server.address}\n**Статус:** {status_text}\n**Игроки:** {server.players_count}/{server.slots}")
    except Exception as e:
        await ctx.send(f"Не удалось получить статус: {e}")

@bot.command(name='start')
async def start_server(ctx):
    await ctx.send("Отправляю запрос на запуск сервера Aternos...")
    try:
        session_cookie = os.getenv("ATERNOS_SESSION")
        if not session_cookie:
            await ctx.send("Ошибка: Не задана переменная ATERNOS_SESSION в Render!")
            return

        aternos = Client.from_minicookie(session_cookie)
        servers = aternos.list_servers()
        
        if not servers:
            await ctx.send("Не найдено ни одного сервера Aternos.")
            return

        server = servers[0]
        server.start()
        await ctx.send("🚀 Запрос на запуск успешно отправлен! Сервер скоро включится.")
    except Exception as e:
        await ctx.send(f"Ошибка при запуске: {e}")

# --- ЗАПУСК ---
if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке, чтобы Render видел открытый порт 10000
    keep_alive()
    
    # Запуск Discord бота
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("Ошибка: Не найден токен DISCORD_TOKEN в переменных окружения!")
