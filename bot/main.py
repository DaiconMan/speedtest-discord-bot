import discord
from discord.ext import tasks
import os
from speedtest import run_speedtest, get_ping_status, get_flag
import asyncio

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
    speedtest_loop.start()

@tasks.loop(hours=1)
async def speedtest_loop():
    global last_result
    channel = client.get_channel(CHANNEL_ID)
    result = run_speedtest()
    embed = discord.Embed(title="📡 Speedtest.net Result", color=discord.Color.blue())

    embed.add_field(name="ISP", value=result["isp"])
    embed.add_field(name="Server", value=f"{get_flag(result['country_code'])} {result['server']}")
    embed.add_field(name="Download", value=f"{result['download']} Mbps {diff(last_result, result, 'download')}")
    embed.add_field(name="Upload", value=f"{result['upload']} Mbps {diff(last_result, result, 'upload')}")
    embed.add_field(name="Ping", value=f"{result['ping']} ms {get_ping_status(result['ping'])}")
    embed.set_footer(text=f"{result['timestamp']}")

    await channel.send(embed=embed)
    await client.change_presence(activity=discord.Game(name=f"Ping: {result['ping']} ms"))

    last_result = result

def diff(prev, curr, key):
    if not prev:
        return ""
    delta = round(curr[key] - prev[key], 2)
    emoji = "🟢" if delta >= 0 else "🔴"
    return f"({delta:+} {emoji})"

client.run(TOKEN)
