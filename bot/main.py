import discord
from discord.ext import tasks
import os
import asyncio
from speedtest import run_speedtest, get_ping_status, get_flag
from datetime import datetime, timedelta

TOKEN_PATH = "/run/secrets/DISCORD_TOKEN"
CHANNEL_ID_PATH = "/run/secrets/DISCORD_CHANNEL_ID"

with open(TOKEN_PATH) as f:
    TOKEN = f.read().strip()

with open(CHANNEL_ID_PATH) as f:
    CHANNEL_ID = int(f.read().strip())

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_result = None

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await post_speedtest()  # 初回即時投稿
    speedtest_scheduler.start()
    ping_status_loop.start()

@tasks.loop(minutes=1)
async def speedtest_scheduler():
    now = datetime.now()
    if now.minute == 0:
        await post_speedtest()

@tasks.loop(minutes=5)
async def ping_status_loop():
    result = run_speedtest()
    ping = result["ping"]
    await client.change_presence(activity=discord.Game(name=f"Ping: {ping} ms"))

async def post_speedtest():
    global last_result
    channel = client.get_channel(CHANNEL_ID)
    result = run_speedtest()

    embed = discord.Embed(title="📡 Speedtest.net Result", color=discord.Color.blue())

    embed.add_field(name="ISP", value=result["isp"], inline=True)
    embed.add_field(name="Server", value=f"{get_flag(result['country_code'])} {result['server']} ({result['country_code']})", inline=True)
    embed.add_field(name="", value="", inline=True)

    embed.add_field(name="Download", value=f"{result['download']} Mbps {diff(last_result, result, 'download')}", inline=True)
    embed.add_field(name="Upload", value=f"{result['upload']} Mbps {diff(last_result, result, 'upload')}", inline=True)
    embed.add_field(name="Ping", value=f"{result['ping']} ms {get_ping_status(result['ping'])}", inline=True)

    embed.set_footer(text=result["timestamp"])

    await channel.send(embed=embed)
    last_result = result

def diff(prev, curr, key):
    if not prev:
        return ""
    delta = round(curr[key] - prev[key], 2)
    emoji = "🟢" if delta >= 0 else "🔴"
    return f"({delta:+.2f} {emoji})"

client.run(TOKEN)
